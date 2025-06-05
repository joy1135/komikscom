<template>
  <div class="min-h-screen bg-white text-white flex">
    <!-- Основной контент -->
    <div class="w-3/4 bg-neutral-900 p-4">
      <h2 class="text-xl font-bold mb-4">Избранное</h2>

      <input
        type="text"
        v-model="searchQuery"
        placeholder="Поиск по названию"
        class="w-full p-2 rounded bg-neutral-800 text-white mb-4"
      />

      <div v-if="loading" class="flex justify-center items-center h-64">
        <span class="text-lg">Загрузка избранного...</span>
      </div>

      <div v-else-if="error" class="flex justify-center items-center h-64">
        <span class="text-red-500 text-lg">{{ error }}</span>
      </div>

      <div v-else-if="comics.length === 0" class="flex justify-center items-center h-64">
        <span class="text-yellow-500 text-lg">У вас пока нет избранных комиксов</span>
      </div>

      <div v-else>
        <div class="grid grid-cols-5 gap-4">
          <div
            v-for="comic in paginatedComics"
            :key="comic.id"
            class="bg-black p-2 rounded shadow-md flex flex-col items-center hover:scale-105 transition-transform"
          >
            <RouterLink
              :to="`/comics/${comic.id}`"
              class="w-full flex flex-col items-center"
            >
              <img
                :src="getFullImageUrl(comic.img)" 
                @error="handleImageError"
                alt="Cover" 
                class="w-full h-48 object-cover rounded"
              />
              <div class="mt-2 text-center">
                <div class="font-bold text-sm">{{ truncateString(comic.title, 20) }}</div>
                <div class="text-xs text-gray-400">{{ comic.author }}</div>
                <div class="text-xs text-yellow-400 mt-1">
                  ★ {{ comic.average_rating ?? "—" }}
                </div>
              </div>
            </RouterLink>
          </div>
        </div>

        <!-- Пагинация -->
        <div class="flex justify-center mt-6 space-x-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-4 py-2 bg-gray-700 rounded disabled:opacity-50 hover:bg-gray-600 transition"
          >
            Назад
          </button>
          <span class="px-4 py-2 bg-gray-800 rounded">
            Страница {{ currentPage }} из {{ totalPages }}
          </span>
          <button
            @click="currentPage++"
            :disabled="currentPage >= totalPages"
            class="px-4 py-2 bg-gray-700 rounded disabled:opacity-50 hover:bg-gray-600 transition"
          >
            Вперед
          </button>
        </div>
      </div>
    </div>

    <!-- Боковая панель -->
    <div class="w-1/4 bg-black p-4">
      <div class="bg-gray-900 p-4 rounded mb-4">
        <h3 class="font-semibold mb-2">Ваше избранное</h3>
        <p class="text-sm text-gray-300">
          Здесь собраны все комиксы, которые вы добавили в избранное.
        </p>
      </div>
      
      <div class="bg-gray-900 p-4 rounded">
        <h3 class="font-semibold mb-2">Статистика</h3>
        <div class="flex justify-between mb-1">
          <span class="text-sm">Всего комиксов:</span>
          <span class="text-red-500 font-medium">{{ comics.length }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-sm">Текущая страница:</span>
          <span class="text-red-500 font-medium">{{ currentPage }}/{{ totalPages }}</span>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth'
import { RouterLink } from 'vue-router';

const apiUrl = import.meta.env.VITE_API_URL;
const API_BASE_URL = import.meta.env.VITE_API_URL1;

const userStore = useAuthStore();
const comics = ref([]);
const loading = ref(true);
const error = ref('');
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 5;

function truncateString(str, maxLength) {
  if (str.length <= maxLength) {
    return str; // Возвращаем строку без изменений, если она короче maxLength
  }
  
  if (maxLength <= 3) {
    return str.slice(0, maxLength); // Без многоточия, если не хватает места
  }
  
  return str.slice(0, maxLength - 3) + '...'; // Обрезаем и добавляем ... (общая длина = maxLength)
}
// Получение изображения
const getFullImageUrl = (imgPath) => {
  if (!imgPath) return '';
  
  if (imgPath.startsWith('http')) return imgPath;
  if (imgPath.startsWith('//')) return window.location.protocol + imgPath;
  if (imgPath.startsWith('/')) return API_BASE_URL + imgPath;
  
  return API_BASE_URL + "/" + imgPath;
};

// Обработка ошибок изображений
const handleImageError = (event) => {
  event.target.src = 'https://dummyimage.com/100x150/000/fff&text=Cover+Error';
};

// Фильтрация комиксов
const filteredComics = computed(() => {
  if (!searchQuery.value.trim()) return comics.value;
  
  const query = searchQuery.value.toLowerCase().trim();
  return comics.value.filter(c => 
    c.title?.toLowerCase().includes(query)
  );
});

// Пагинация
const totalPages = computed(() => {
  return Math.ceil(filteredComics.value.length / itemsPerPage);
});

const paginatedComics = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredComics.value.slice(start, start + itemsPerPage);
});

// Загрузка избранных комиксов
async function fetchFavorites() {
  try {
    loading.value = true;
    
    const nick = userStore.nickname;
    console.log(nick);
    if (!nick) throw new Error('Пользователь не авторизован');
    
    const response = await fetch(`${apiUrl}/comic/favorites/${nick}`);
    if (!response.ok) throw new Error('Ошибка загрузки данных');
    
    comics.value = await response.json();
  } catch (err) {
    console.error('Ошибка:', err);
    error.value = err.message || 'Не удалось загрузить избранное';
  } finally {
    loading.value = false;
  }
}

onMounted(fetchFavorites, userStore.initAuthState());
</script>

<style scoped>
img {
  width: 100px;
  height: 150px;
  object-fit: cover;
}

a {
  color: inherit;
  text-decoration: none;
}

/* Адаптивность */
@media (max-width: 1024px) {
  .flex {
    flex-direction: column;
  }

  .w-3\/4 {
    width: 100% !important;
  }

  .w-1\/4 {
    display: none !important;
  }

  .grid-cols-5 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .text-xl {
    font-size: 1.25rem;
  }

  .text-lg {
    font-size: 1.125rem;
  }

  .text-sm {
    font-size: 0.875rem;
  }

  .p-4 {
    padding: 1rem;
  }

  .mb-4 {
    margin-bottom: 1rem;
  }
}

@media (max-width: 768px) {
  .grid-cols-5 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 480px) {
  .grid-cols-5 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }

  .text-xs {
    font-size: 0.75rem;
  }

  .p-2 {
    padding: 0.5rem;
  }
}



</style>