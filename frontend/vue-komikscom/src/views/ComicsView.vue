<!-- src/views/ComicsView.vue -->
<template>
  <div class="bg-white text-white min-h-screen">
    <div
      class="h-48 bg-cover bg-center"
      :style="{ backgroundImage: `url(${comics.bg})` }"
    ></div>

    <div class="max-w-6xl mx-auto -mt-20 flex gap-6 p-6">
     
      <div class="w-1/4 bg-black p-4 rounded-lg shadow">
        <img
          :src="comics.cover"
          alt="Cover"
          class="w-full h-64 object-cover rounded-lg mb-4"
        />

        <button class="w-full bg-red-600 text-white py-2 rounded mb-2 hover:bg-red-700">
          Начать читать
        </button>
        <button class="w-full bg-gray-500 text-white py-2 rounded mb-4">Комментарии</button>

        <div class="space-y-2 text-sm">
          <div><span class="font-semibold">Дата выпуска:</span> {{ comics.date }}</div>
          <div><span class="font-semibold">Автор:</span> {{ comics.author }}</div>
          <div>
            <span class="font-semibold">Жанры:</span>
            <div>{{ comics.genres.join(', ') }}</div>
          </div>
          <div><span class="font-semibold">Оценка:</span> {{ comics.rating }}</div>
          <div><span class="font-semibold">Кол-во глав:</span> {{ comics.chapters.length }}</div>
        </div>
      </div>

      
      <div class="flex-1 bg-neutral-900 p-6 rounded-lg shadow">
        <div class="flex justify-between items-center mb-4">
          <h1 class="text-2xl font-bold">{{ comics.title }}</h1>
          <button class="text-2xl">♡</button>
        </div>

        <div class="mb-4">
          <h2 class="font-semibold mb-1">Описание:</h2>
          <p class="text-sm">{{ comics.description }}</p>
        </div>

        <div>
          <h2 class="font-semibold mb-2">Главы:</h2>
          <ul class="space-y-1">
            <li
              v-for="(chapter, index) in comics.chapters"
              :key="index"
              class="bg-neutral-800 px-4 py-2 rounded"
            >
              {{ chapter }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, onBeforeRouteUpdate } from 'vue-router'

const route = useRoute()
const comics = ref({
  title: '',
  description: '',
  author: '',
  date: '',
  rating: 0,
  genres: [],
  chapters: [],
  cover: '',
  bg: ''
})

const fetchComicsById = (id) => {
  const mock = {
    '1': {
      title: 'Шрек 2',
      description:
        'Официальное продолжение знаменитого и великого мультфильма Шрек...',
      author: 'Ричард Карлсон',
      date: '18.11.1900',
      rating: 10,
      genres: ['Спорт', 'Детектив'],
      chapters: ['Том 1 Глава 1', 'Том 1 Глава 2', 'Том 1 Глава 3'],
      cover: 'https://upload.wikimedia.org/wikipedia/en/3/39/Shrek.jpg',
      bg: 'https://upload.wikimedia.org/wikipedia/en/3/39/Shrek.jpg'
    }
  }

  comics.value = mock[id] || {
    title: 'Не найдено',
    description: 'Книга не найдена',
    author: '',
    date: '',
    rating: 0,
    genres: [],
    chapters: [],
    cover: '',
    bg: ''
  }
}

onMounted(() => {
  fetchComicsById(route.params.id)
})

onBeforeRouteUpdate((to) => {
  fetchComicsById(to.params.id)
})
</script>
