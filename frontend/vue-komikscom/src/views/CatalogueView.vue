<template>
  <div class="min-h-screen bg-white text-white flex">
    <!-- Каталог -->
    <div class="w-3/4 bg-neutral-900 p-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Каталог</h2>
          <select
    v-model="sortOption"
    @change="fetchSortedComics"
    class="bg-gray-700 text-white px-4 py-1 rounded"
  >
    <option disabled value="">Сортировка</option>
    <option value="popular">По популярности</option>
    <option value="avg_rat">По средней оценке</option>
    <option value="sort_asc">По названию (А–Я)</option>
  </select>
      </div>

      <input
        type="text"
        placeholder="Поиск по названию"
        class="w-full p-2 rounded bg-neutral-800 text-white"
      />

      <div class="grid grid-cols-5 gap-4 mt-4">
        <div
          v-for="comic in comics"
          :key="comic.id"
          class="bg-black p-2 rounded shadow-md flex flex-col items-center"
        >
          <img
            src="https://dummyimage.com/100x150"
            alt="cover"
            class="w-24 h-32 object-cover rounded"
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
        <label v-for="genre in genres" :key="genre.id" class="flex items-center">
          <input 
            type="checkbox" 
            :value="genre.id" 
            v-model="selectedGenres" 
            class="mr-2"
          /> 
          {{ genre.name }}
        </label>
      </div>

      <h3 class="text-lg font-semibold mb-2">Оценка</h3>
      <div class="flex flex-col space-y-1">
        <label v-for="score in 10" :key="score" class="flex items-center">
          <input 
            type="radio" 
            :value="score" 
            v-model="minRating" 
            name="rating" 
            class="mr-2"
          />
          {{ score }}+
        </label>
        <button 
          @click="minRating = null"
          class="text-sm text-blue-400 mt-1 underline"
        >
          Сбросить оценку
        </button>
          <!-- Применить фильтры -->
      <div class="mt-6">
        <button
          @click="applyFilters"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded transition"
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

const genres = ref([]);
const selectedGenres = ref([]);
const minRating = ref(null);
const loading = ref(true);
const genresError = ref('');
const comics = ref([]);
const sortOption = ref('');

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

    const response = await fetch(`${apiUrl}/comic/filter?${params.toString()}`);
    const data = await response.json();
    comics.value = data;
  } catch (err) {
    console.error('Ошибка при получении комиксов:', err);
  }
}
async function fetchSortedComics() {
  if (!sortOption.value) return;

  try {
    const response = await fetch(`${apiUrl}/comic/${sortOption.value}`);
    const data = await response.json();
    comics.value = data;
  } catch (error) {
    console.error('Ошибка при сортировке:', error);
  }
}

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

input[type="checkbox"],
input[type="radio"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}
</style>
