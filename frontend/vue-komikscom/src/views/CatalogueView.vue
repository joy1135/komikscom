<template>
  <div class="min-h-screen bg-white text-white flex">
    <!-- Каталог -->
    <div class="w-3/4 bg-neutral-900 p-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Каталог</h2>
        <select
          v-model="sortOption"
          @change="applyFilters(true)"
          class="bg-gray-700 text-white px-4 py-1 rounded"
        >
          <option disabled value="">Сортировка</option>
          <option value="popular">По популярности</option>
          <option value="avg_rating">По средней оценке</option>
          <option value="asc">По названию (А–Я)</option>
        </select>
      </div>

     

      <div class="grid grid-cols-5 gap-4 mt-4">
        <router-link
          v-for="comic in comics"
          :key="comic.id"
          :to="`/comics/${comic.id}`"
          class="bg-black p-2 rounded shadow-md flex flex-col items-center hover:scale-105 transition-transform"
        >
          <img
            :src="getFullImageUrl(comic.img)"
            @error="handleImageError"
            alt="Cover"
            class="w-full h-48 object-cover"
          />
          <div class="mt-2 text-center">
            <span class="font-bold text-sm">{{ truncateString(comic.title, 20) }} </span>
            <div class="text-xs text-gray-400">{{ comic.author }}</div>
            <div class="text-xs text-yellow-400 mt-1">
              ★ {{ comic.average_rating ?? "—" }}
            </div>
          </div>
        </router-link>
      </div>

      <!-- Пагинация -->
      <div class="flex justify-center mt-6 space-x-2">
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="px-4 py-2 bg-gray-700 rounded disabled:opacity-50 hover:bg-gray-600 transition"
        >
          Назад
        </button>
        <span class="px-4 py-2 bg-gray-800 rounded">
          Страница {{ currentPage }}
        </span>
        <button
          @click="nextPage"
          :disabled="!hasNextPage"
          class="px-4 py-2 bg-gray-700 rounded disabled:opacity-50 hover:bg-gray-600 transition"
        >
          Вперед
        </button>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="w-1/4 bg-black p-4">
      <h3 class="text-lg font-semibold mb-2">Жанры</h3>
      <div v-if="loading" class="text-gray-400">Загрузка жанров...</div>
      <div v-else-if="genresError" class="text-red-500">{{ genresError }}</div>
      <div v-else-if="genres.length === 0" class="text-yellow-500">Жанры не найдены</div>
      <div v-else class="flex flex-col space-y-1 mb-4">
        <label
          v-for="genre in genres"
          :key="genre.id"
          class="flex items-center space-x-2 cursor-pointer group"
          @click="toggleGenre(genre.id)"
        >
          <span
            class="w-4 h-4 rounded-full border-2 border-red-500 flex items-center justify-center transition"
            :class="{ 'bg-red-500': selectedGenres.includes(genre.id) }"
          >
            <span
              v-if="selectedGenres.includes(genre.id)"
              class="w-2 h-2 bg-white rounded-full"
            ></span>
          </span>
          <span>{{ genre.name }}</span>
        </label>
      </div>

      <h3 class="text-lg font-semibold mb-2">Оценка</h3>
      <div class="flex flex-col space-y-1">
        <label
          v-for="score in 10"
          :key="score"
          class="flex items-center space-x-2 cursor-pointer group"
          @click="minRating = score"
        >
          <span
            class="w-4 h-4 rounded-full border-2 border-red-500 flex items-center justify-center transition"
            :class="{ 'bg-red-500': minRating === score }"
          >
            <span
              v-if="minRating === score"
              class="w-2 h-2 bg-white rounded-full"
            ></span>
          </span>
          <span>{{ score }}+</span>
        </label>

        <button
          @click="resetFilters"
          class="text-sm text-red-500 mt-1 underline"
        >
          Сбросить фильтры и оценку
        </button>

        <div class="mt-6">
          <button
            @click="applyFilters(true)"
            class="w-full bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded transition"
          >
            Применить фильтры
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const apiUrl = import.meta.env.VITE_API_URL;
const API_BASE_URL = import.meta.env.VITE_API_URL1;

const genres = ref([]);
const selectedGenres = ref([]);
const minRating = ref(null);
const loading = ref(true);
const genresError = ref('');
const comics = ref([]);
const sortOption = ref('');
const searchQuery = ref('');

// Пагинация
const currentPage = ref(1);
const itemsPerPage = ref(10);
const hasNextPage = ref(false);

function truncateString(str, maxLength) {
  if (str.length <= maxLength) {
    return str; // Возвращаем строку без изменений, если она короче maxLength
  }
  
  if (maxLength <= 3) {
    return str.slice(0, maxLength); // Без многоточия, если не хватает места
  }
  
  return str.slice(0, maxLength - 3) + '...'; // Обрезаем и добавляем ... (общая длина = maxLength)
}
const getFullImageUrl = (imgPath) => {
  if (!imgPath) return '';
  
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) {
    return imgPath;
  }
  
  if (imgPath.startsWith('//')) {
    return window.location.protocol + imgPath;
  }
  
  if (imgPath.startsWith('/')) {
    return API_BASE_URL + imgPath;
  }
  
  return API_BASE_URL + "/" + imgPath;
};

const handleImageError = (event) => {
  console.error('Ошибка загрузки изображения:', event.target.src);
  event.target.src = 'https://dummyimage.com/100x150/000/fff&text=Cover+Error';
};

function toggleGenre(id) {
  if (selectedGenres.value.includes(id)) {
    selectedGenres.value = selectedGenres.value.filter(g => g !== id);
  } else {
    selectedGenres.value.push(id);
  }
}

function resetFilters() {
  selectedGenres.value = [];
  minRating.value = null;
  searchQuery.value = '';
  sortOption.value = '';
  currentPage.value = 1;
  applyFilters();
}

async function applyFilters(resetPage = false) {
  if (resetPage) {
    currentPage.value = 1;
  }
  
  try {
    const params = new URLSearchParams();

    selectedGenres.value.forEach(g => params.append('genres', g));
    
    if (minRating.value !== null) {
      params.append('min_rating', minRating.value);
    }
    
    if (sortOption.value) {
      params.append('sort', sortOption.value);
    }
    
    if (searchQuery.value.trim() !== '') {
      params.append('search', searchQuery.value.trim());
    }
    
    params.append('page', currentPage.value);
    params.append('limit', itemsPerPage.value);

    const response = await fetch(`${apiUrl}/comic/comics?${params.toString()}`);
    
    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`);
    }
    
    const data = await response.json();
    comics.value = data;
    
    hasNextPage.value = data.length === itemsPerPage.value;
  } catch (err) {
    console.error('Ошибка при получении комиксов:', err);
    comics.value = [];
    hasNextPage.value = false;
  }
}

function nextPage() {
  currentPage.value++;
  applyFilters();
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
    applyFilters();
  }
}

async function fetchGenres() {
  try {
    const response = await fetch(`${apiUrl}/genre/`);
    
    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`);
    }
    
    const data = await response.json();

    let rawGenres = [];

    if (Array.isArray(data)) rawGenres = data;
    else if (data.data) rawGenres = data.data;
    else if (data.genres) rawGenres = data.genres;
    else if (data.results) rawGenres = data.results;
    else throw new Error('Некорректный формат данных о жанрах');

    genres.value = rawGenres.map((g, i) => ({
      id: g.id ?? i + 1,
      name: g.name ?? "Без названия"
    }));
  } catch (err) {
    console.error('Ошибка при загрузке жанров:', err);
    genresError.value = 'Не удалось загрузить жанры';
    genres.value = [
      { id: 1, name: 'Спорт' },
      { id: 2, name: 'Детектив' },
      { id: 3, name: 'Боевик' }
    ];
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchGenres();
  applyFilters();
});
</script>

<style scoped>
label {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.3s;
  cursor: pointer;
}

label:hover {
  background: #333;
}

img {
  width: 100px;
  height: 150px;
  object-fit: cover;
}
.grid-cols-5 {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 1rem;
}

@media (max-width: 1280px) {
  .grid-cols-5 {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 1024px) {
  .grid-cols-5 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .grid-cols-5 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .w-3\/4,
  .w-1\/4 {
    width: 100% !important;
  }

  .flex {
    flex-direction: column;
  }

  .p-4 {
    padding: 1rem;
  }

  .text-xl {
    font-size: 1.125rem;
  }

  .text-lg {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .grid-cols-5 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }

  .text-sm {
    font-size: 0.85rem;
  }

  .text-xs {
    font-size: 0.75rem;
  }
}
</style>