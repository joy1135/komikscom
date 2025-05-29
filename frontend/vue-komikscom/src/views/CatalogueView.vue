<template>
  <div class="min-h-screen bg-white text-white flex">
    <!-- Каталог -->
    <div class="w-3/4 bg-neutral-900 p-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Каталог</h2>
        <select
          v-model="sortOption"
          @change="applyFilters"
          class="bg-gray-700 text-white px-4 py-1 rounded"
        >
          <option disabled value="">Сортировка</option>
          <option value="popular">По популярности</option>
          <option value="avg_rating">По средней оценке</option>
          <option value="asc">По названию (А–Я)</option>
        </select>
      </div>

      <input
        type="text"
        v-model="searchQuery"
        placeholder="Поиск по названию"
        class="w-full p-2 rounded bg-neutral-800 text-white"
      />

      <div class="grid grid-cols-5 gap-4 mt-4">
        <div
          v-for="comic in filteredComics"
          :key="comic.id"
          class="bg-black p-2 rounded shadow-md flex flex-col items-center"
        >
          <img
            :src="getFullImageUrl(comic.img)" 
            @error="handleImageError"
            alt="Cover" 
          />
          <div class="mt-2 text-center">
            <div class="font-bold text-sm">{{ comic.title }}</div>
            <div class="text-xs text-gray-400">{{ comic.author }}</div>
            <div class="text-xs text-yellow-400 mt-1">★ {{ comic.average_rating ?? "—" }}</div>
          </div>
        </div>
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
            @click="applyFilters"
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
import { ref, onMounted, computed } from 'vue';

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
const getFullImageUrl = (imgPath) => {
  if (!imgPath) return '';
  
  // Если путь уже является абсолютным URL
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) {
    return imgPath;
  }
  
  // Если путь начинается с двойного слеша (//example.com)
  if (imgPath.startsWith('//')) {
    return window.location.protocol + imgPath;
  }
  
  // Если путь абсолютный (начинается с /)
  if (imgPath.startsWith('/')) {
    return API_BASE_URL + imgPath;
  }
  
  // Относительный путь
  return API_BASE_URL +"/"+ imgPath;
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
  applyFilters();
}

async function fetchGenres() {
  try {
    const response = await fetch(`${apiUrl}/genre`);
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

async function applyFilters() {
  try {
    const params = new URLSearchParams();

    selectedGenres.value.forEach(g => params.append('genres', g));
    if (minRating.value !== null) {
      params.append('min_rating', minRating.value);
    }
    if (sortOption.value) {
      params.append('sort', sortOption.value);
    }

    const response = await fetch(`${apiUrl}/comic/comics?${params.toString()}`);
    const data = await response.json();
    comics.value = data;
  } catch (err) {
    console.error('Ошибка при получении комиксов:', err);
  }
}

const filteredComics = computed(() => {
  const query = searchQuery.value.toLowerCase().trim();
  if (!query) return comics.value;
  return comics.value.filter(c =>
    c.title?.toLowerCase().includes(query)
  );
});

onMounted(() => {
  fetchGenres();
  applyFilters(); // Загрузить при инициализации
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
</style>
