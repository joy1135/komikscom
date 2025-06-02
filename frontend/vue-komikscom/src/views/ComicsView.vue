<template>
  <div class="bg-white text-white min-h-screen">
    <div class="h-48 bg-cover bg-center" :style="{ backgroundImage: `url(${comics.bg})` }"></div>

    <div class="max-w-6xl mx-auto -mt-20 flex gap-6 p-6">
      <!-- Левая панель -->
      <div class="w-1/4 bg-black p-4 rounded-lg shadow">
        <img :src="comics.cover" alt="Cover" class="w-full h-64 object-cover rounded-lg mb-4" />

        <button
          class="w-full bg-red-600 text-white py-2 rounded mb-2 hover:bg-red-700"
          @click="startReading"
        >
          Начать читать
        </button>
        <button class="w-full bg-gray-500 text-white py-2 rounded mb-4">Комментарии</button>

        <div class="space-y-2 text-sm">
          <div><span class="font-semibold">Дата выпуска:</span> {{ comics.date }}</div>
          <div><span class="font-semibold">Автор:</span> {{ comics.author }}</div>
          <div><span class="font-semibold">Жанры:</span> {{ comics.genres.join(', ') }}</div>
          <div><span class="font-semibold">Оценка:</span> {{ comics.rating }}</div>
          <div>
            <span class="font-semibold">Кол-во глав:</span> 
            {{ comics.chaptersCount }}
          </div>
        </div>
      </div>

      <!-- Правая панель -->
      <div class="flex-1 bg-neutral-900 p-6 rounded-lg shadow">
        <div class="flex justify-between items-center mb-4">
          <h1 class="text-2xl font-bold">{{ comics.title }}</h1>
          <button 
            class="text-2xl transition-colors duration-300"
            :class="isFavorite ? 'text-red-500' : 'text-gray-400 hover:text-white'"
            @click="toggleFavorite"
            :disabled="favoriteLoading"
          >
            <span v-if="favoriteLoading">...</span>
            <span v-else>{{ isFavorite ? '♥' : '♡' }}</span>

          </button>
        </div>

        <div class="mb-4">
          <h2 class="font-semibold mb-1">Описание:</h2>
          <p class="text-sm whitespace-pre-line">{{ comics.description }}</p>
        </div>

        <!-- Том и главы -->
        <div>
          <h2 class="font-semibold mb-2">Тома и главы:</h2>
          
          <div v-if="loading" class="text-center py-4">Загрузка глав...</div>
          
          <div v-else-if="volumes.length === 0" class="text-gray-400">
            Нет доступных глав
          </div>
          
          <div v-else>
            <div v-for="volume in volumes" :key="volume.id" class="mb-4">
              <h3 class="text-lg font-bold mb-2">Том {{ volume.number }}</h3>
              <ul class="space-y-1">
                <li
                  v-for="chapter in sortedChapters(volume.chapters)"
                  :key="chapter.id"
                  class="bg-neutral-800 px-4 py-2 rounded hover:bg-neutral-700 cursor-pointer"
                  @click="goToReader(comics.id, chapter.id)"
                >
                  <div class="flex items-center">
                    <span>
                      Глава {{ chapter.number }} 
                      <span v-if="chapter.title">- {{ chapter.title }}</span>
                    </span>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL 

const authStore = useAuthStore()

const comicData = ref(null)
const loading = ref(true)
const isFavorite = ref(false)
const favoriteLoading = ref(false)
const comicId = ref(0)

// Преобразуем данные комикса
const comics = computed(() => {
  if (!comicData.value) return emptyComic()

  return {
    id: comicData.value.id,
    title: comicData.value.title,
    description: comicData.value.desc || 'Описание отсутствует',
    author: comicData.value.user?.nick || 'Неизвестен',
    date: formatDate(comicData.value.date_of_out),
    rating: comicData.value.average_rating?.toFixed(1) || '0.0',
    genres: comicData.value.genres?.map(g => g.name) || [],
    cover: comicData.value.img ? `${API_URL}/${comicData.value.img}` : '/placeholder-cover.jpg',
    bg: comicData.value.img ? `${API_URL}/${comicData.value.img}` : '/placeholder-bg.jpg',
    chaptersCount: comicData.value.volumes?.reduce(
      (total, volume) => total + (volume.chapters?.length || 0), 0
    ) || 0
  }
})

const volumes = computed(() => {
  if (!comicData.value?.volumes) return []
  return [...comicData.value.volumes].sort((a, b) => a.number - b.number)
})

const sortedChapters = (chapters) => {
  if (!chapters) return []
  return [...chapters].sort((a, b) => a.number - b.number)
}

const fetchComicsById = async (id) => {
  try {
    loading.value = true
    const response = await fetch(`${API_URL}/comic/comics/${id}`)
    if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`)
    const data = await response.json()
    comicData.value = data
    comicId.value = data.id
    return data
  } catch (err) {
    console.error('Ошибка при загрузке комикса:', err)
    comicData.value = emptyComic()
    comicId.value = 0
    return emptyComic()
  } finally {
    loading.value = false
  }
}

const checkFavoriteStatus = async () => {
  if (!authStore.isLoggedIn || !comicId.value) {
    isFavorite.value = false
    return
  }

  try {
    favoriteLoading.value = true
    const response = await fetch(`${API_URL}/comic/${comicId.value}/is_favorite`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      isFavorite.value = data
    } else {
      isFavorite.value = false
    }
  } catch (err) {
    console.error('Ошибка проверки избранного:', err)
    isFavorite.value = false
  } finally {
    favoriteLoading.value = false
  }
  
}

const toggleFavorite = async () => {
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }

  if (!comicId.value) return
  
  try {
    favoriteLoading.value = true
    const currentState = isFavorite.value
    isFavorite.value = !currentState

    if (currentState) {
      await removeFromFavorites()
    } else {
      await addToFavorites()
    }
  } catch (err) {
    console.error('Ошибка обновления избранного:', err)
    isFavorite.value = !isFavorite.value
  } finally {
    favoriteLoading.value = false
  }
}

const addToFavorites = async () => {
  const response = await fetch(`${API_URL}/comic/${comicId.value}/favorite`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  if (!response.ok) throw new Error('Не удалось добавить в избранное')
}

const removeFromFavorites = async () => {
  const response = await fetch(`${API_URL}/comic/${comicId.value}/del_favorite`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  if (!response.ok) throw new Error('Не удалось удалить из избранного')
}

const goToReader = (comicId, chapterId) => {
  router.push({
    name: 'reader',
    params: {
      comic_id: comicId,
      chapter_id: chapterId,
      page_number: 1
    }
  })
}

const startReading = () => {
  if (!comicData.value?.volumes?.length) return
  const firstVolumeWithChapters = comicData.value.volumes.find(v => v.chapters?.length)
  if (!firstVolumeWithChapters) return
  const firstChapter = sortedChapters(firstVolumeWithChapters.chapters)[0]
  if (!firstChapter) return
  goToReader(comicData.value.id, firstChapter.id)
}

const formatDate = (dateString) => {
  if (!dateString) return 'Дата неизвестна'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch {
    return dateString
  }
}

const emptyComic = () => ({
  id: 0,
  title: 'Не найдено',
  description: 'Комикс не найден или произошла ошибка загрузки',
  author: '',
  date: '',
  rating: '0.0',
  genres: [],
  cover: '/placeholder-cover.jpg',
  bg: '/placeholder-bg.jpg',
  chaptersCount: 0
})

const loadComicData = async () => {
  const data = await fetchComicsById(route.params.id)

  if (data?.id && authStore.isLoggedIn) {
    await checkFavoriteStatus()
  } else {
    isFavorite.value = false
  }
}

watch(() => route.params.id, () => {
  comicData.value = null
  comicId.value = 0
  isFavorite.value = false
  loadComicData()
})

watch(() => authStore.isLoggedIn, async (isLoggedIn) => {
  if (isLoggedIn && comicId.value > 0) {
    await checkFavoriteStatus()
  } else {
    isFavorite.value = false
  }
})

onMounted(() => {
  loadComicData()
})
</script>
