<template>
  <div class="bg-white text-white min-h-screen">
    <div class="h-48 bg-cover bg-center" :style="{ backgroundImage: `url(${comics.bg})` }"></div>

    <div class="max-w-6xl mx-auto -mt-20 flex gap-6 p-6">
      <!-- Левая панель -->
      <div class="w-1/4 bg-neutral-900 p-4 rounded-lg shadow flex flex-col h-full">
        <img :src="comics.cover" alt="Cover" class="w-full h-64 object-contain rounded-lg mb-4" />

        <button
          class="w-full bg-red-600 text-white py-2 rounded mb-2 hover:bg-red-700"
          @click="startReading"
        >
          Начать читать
        </button>

        <!-- Оценка комикса -->
        <div class="mb-4">
          <h3 class="font-semibold mb-1">Оценить комикс:</h3>
          <select v-model.number="ratingValue" class="w-full text-black p-1 rounded mb-2">
            <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
          </select>
          <button
            class="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded"
            :disabled="ratingLoading || !authStore.isLoggedIn"
            @click="submitRating"
          >
            {{ ratingLoading ? 'Отправка...' : 'Отправить оценку' }}
          </button>
          <div v-if="ratingError" class="text-red-500 mt-1 text-sm">{{ ratingError }}</div>
        </div>

        <!-- Информация о комиксе -->
        <div class="space-y-2 text-sm flex-grow">
          <div><span class="font-semibold">Дата выпуска:</span> {{ comics.date }}</div>
          <div><span class="font-semibold">Автор:</span> {{ comics.author }}</div>
          <div><span class="font-semibold">Жанры:</span> {{ comics.genres.join(', ') }}</div>
          <div><span class="font-semibold">Средняя оценка:</span> {{ comics.rating }}</div>
          <div><span class="font-semibold">Кол-во глав:</span> {{ comics.chaptersCount }}</div>
        </div>

        <!-- Управление комиксом -->
        <div v-if="isAdminOrAuthor" class="mt-4 border-t border-gray-700 pt-4">
          <h3 class="font-semibold mb-2">Управление комиксом:</h3>
        
          <!-- Загрузка страниц --> 
          <div v-if="selectedChapterForUpload" class="mt-2">
            <input 
              type="file" 
              ref="fileInput" 
              multiple 
              accept="image/*" 
              class="hidden" 
              @change="handleFileUpload"
            >
            <button
              class="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 rounded mb-2"
              @click="triggerFileInput"
            >
              Загрузить страницы
            </button>
            <div v-if="uploadingPages" class="text-center text-sm text-gray-400">Загрузка...</div>
            <div v-if="uploadError" class="text-red-500 text-sm">{{ uploadError }}</div>
          </div>
        </div>
      </div>

      <!-- Правая панель -->
      <div class="flex-1 bg-neutral-900 p-6 rounded-lg shadow flex flex-col">
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
        <div class="flex-grow overflow-y-auto">
          <div class="flex justify-between items-center mb-2">
            <h2 class="font-semibold">Тома и главы:</h2>
            <!-- Кнопка добавления тома для админа/автора -->
            <button 
              v-if="isAdminOrAuthor"
              @click="createVolume"
              class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
              :disabled="volumeLoading"
            >
              + Добавить том
            </button>
          </div>
          
          <div v-if="loading" class="text-center py-4">Загрузка глав...</div>
          
          <div v-else-if="volumes.length === 0" class="text-gray-400">
            Нет доступных глав
          </div>
          
          <div v-else>
            <div v-for="volume in volumes" :key="volume.id" class="mb-4">
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-bold">Том {{ volume.number }}</h3>
                <div v-if="isAdminOrAuthor">
                  <!-- Кнопка добавления главы -->
                  <button 
                    @click="createChapter(volume.id)"
                    class="bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded text-sm mr-2"
                    :disabled="chapterLoading"
                  >
                    + Глава
                  </button>
                  <!-- Кнопка удаления тома -->
                  <button 
                    @click="deleteVolume(volume.id)"
                    class="bg-red-600 hover:bg-red-700 text-white px-2 py-1 rounded text-sm"
                    :disabled="deletingVolume === volume.id"
                  >
                    Удалить
                  </button>
                </div>
              </div>
              <ul class="space-y-1">
                <li
                  v-for="chapter in sortedChapters(volume.chapters)"
                  :key="chapter.id"
                  class="bg-neutral-800 px-4 py-2 rounded hover:bg-neutral-700"
                >
                  <div class="flex justify-between items-center">
                    <span class="cursor-pointer" @click="goToReader(comics.id, chapter.id)">
                      Глава {{ chapter.number }} 
                      <span v-if="chapter.title">- {{ chapter.title }}</span>
                    </span>
                    <div>
                      <!-- Кнопка загрузки страниц -->
                      <button 
                        v-if="isAdminOrAuthor"
                        @click.stop="selectChapterForUpload(chapter.id)"
                        class="text-blue-400 hover:text-blue-600 mr-2 text-sm"
                        :class="{ 'text-blue-600 font-bold': selectedChapterForUpload === chapter.id }"
                      >
                        Страницы
                      </button>
                      <!-- Кнопка удаления главы -->
                      <button 
                        v-if="isAdminOrAuthor"
                        @click.stop="deleteChapter(chapter.id)"
                        class="text-red-500 hover:text-red-700"
                        :disabled="deletingChapter === chapter.id"
                      >
                        Удалить
                      </button>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Комментарии -->
        <div class="mt-6 border-t border-gray-700 pt-4">
          <h2 class="text-xl font-semibold mb-4">Комментарии</h2>

          <div v-if="loadingComments" class="text-center py-4 text-gray-400">Загрузка комментариев...</div>
          <div v-else-if="comments.length === 0" class="text-gray-400 mb-4">Комментариев пока нет</div>
          <div v-else class="max-h-64 overflow-y-auto mb-4">
            <div v-for="comment in comments" :key="comment.id" class="mb-3 border-b border-gray-700 pb-2">
              <p class="text-gray-400 font-semibold">
                <span v-if="comment.user">{{ comment.user.nick }}</span>
                <span v-else>Аноним</span>
                <small class="ml-2 text-xs text-gray-600">{{ formatDate(comment.created_at) }}</small>
              </p>
              <p class="text-white whitespace-pre-wrap">{{ comment.comment }}</p>
            </div>
          </div>

          <!-- Форма добавления комментария -->
          <form @submit.prevent="submitComment">
            <textarea
              v-model="newComment"
              rows="3"
              placeholder="Оставьте комментарий"
              class="w-full p-2 rounded bg-gray-800 text-white resize-none"
              :disabled="!authStore.isLoggedIn || commentLoading"
              required
            ></textarea>
            <button
              type="submit"
              class="mt-2 w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded"
              :disabled="commentLoading || !authStore.isLoggedIn"
            >
              {{ commentLoading ? 'Отправка...' : 'Отправить комментарий' }}
            </button>
            <div v-if="commentError" class="text-red-500 mt-1 text-sm">{{ commentError }}</div>
            <div v-if="!authStore.isLoggedIn" class="text-yellow-400 mt-1 text-sm">
              Чтобы оставить комментарий, нужно <router-link to="/login" class="underline">войти</router-link>.
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL
const API_URL1 = import.meta.env.VITE_API_URL1
const authStore = useAuthStore()
const fileInput = ref(null)

const comicData = ref(null)
const loading = ref(true)
const comicId = ref(0)

const isFavorite = ref(false)
const favoriteLoading = ref(false)

const comments = ref([])
const loadingComments = ref(false)
const commentLoading = ref(false)
const commentError = ref('')
const newComment = ref('')

const ratingValue = ref(5)
const ratingLoading = ref(false)
const ratingError = ref('')

// Управление томами/главами
const volumeLoading = ref(false)
const chapterLoading = ref(false)
const deletingVolume = ref(null)
const deletingChapter = ref(null)
const deletingComic = ref(false)
const selectedChapterForUpload = ref(null)
const uploadingPages = ref(false)
const uploadError = ref('')
// проверка является ли пользователь автором комикса
const isAuthorOfComic = computed(() => {
  return comicData.value?.user?.id === authStore.userId
})

// Проверка прав (админ=1, автор=3)
const isAdminOrAuthor = computed(() => {
  return authStore.isLoggedIn && (authStore.role === 1 || authStore.role === 3) && isAuthorOfComic.value
  
})

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
    cover: comicData.value.img ? `${API_URL1}/${comicData.value.img}` : '/placeholder-cover.jpg',
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
  loading.value = true
  try {
    const res = await fetch(`${API_URL}/comic/comics/${id}`)
    if (!res.ok) throw new Error(`Ошибка HTTP: ${res.status}`)
    const data = await res.json()
    comicData.value = data
    comicId.value = data.id
  } catch (err) {
    console.error('Ошибка загрузки комикса:', err)
    comicData.value = emptyComic()
    comicId.value = 0
  } finally {
    loading.value = false
  }
}

const checkFavoriteStatus = async () => {
  if (!authStore.isLoggedIn || !comicId.value) {
    isFavorite.value = false
    return
  }
  favoriteLoading.value = true
  try {
    const res = await fetch(`${API_URL}/comic/${comicId.value}/is_favorite`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
    })
    if (res.ok) {
      const data = await res.json()
      isFavorite.value = data
    } else {
      isFavorite.value = false
    }
  } catch {
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

  favoriteLoading.value = true
  try {
    if (isFavorite.value) {
      const res = await fetch(`${API_URL}/comic/${comicId.value}/del_favorite`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      })
      if (!res.ok) throw new Error('Ошибка удаления из избранного')
      isFavorite.value = false
    } else {
      const res = await fetch(`${API_URL}/comic/${comicId.value}/favorite`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      })
      if (!res.ok) throw new Error('Ошибка добавления в избранное')
      isFavorite.value = true
    }
  } catch (err) {
    alert(err.message)
  } finally {
    favoriteLoading.value = false
  }
}

const fetchComments = async () => {
  if (!comicId.value) return
  loadingComments.value = true
  commentError.value = ''
  try {
    const res = await fetch(`${API_URL}/comm/${comicId.value}/comments`)
    if (!res.ok) throw new Error(`Ошибка загрузки комментариев: ${res.status}`)
    const data = await res.json()
    comments.value = data
  } catch (err) {
    commentError.value = 'Ошибка загрузки комментариев'
    comments.value = []
  } finally {
    loadingComments.value = false
  }
}

const submitComment = async () => {
  if (!authStore.isLoggedIn) {
    commentError.value = 'Для комментирования нужно войти в аккаунт'
    return
  }
  if (!newComment.value.trim()) return
  commentLoading.value = true
  commentError.value = ''
  try {
    const comment = JSON.stringify({
        comment: newComment.value.trim(),
        comicID: comicId.value,
        userID: authStore.userId,
        user: {
          email: authStore.email,
          nick: authStore.nickname}
      })
    const res = await fetch(`${API_URL}/comm/${comicId.value}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      },
      body: comment
    })
    if (!res.ok) throw new Error(`Ошибка отправки комментария: ${res.status}`)
    newComment.value = ''
    await fetchComments()
  } catch (err) {
    commentError.value = err.message || 'Ошибка отправки комментария'
  } finally {
    commentLoading.value = false
  }
}

const submitRating = async () => {
  if (!authStore.isLoggedIn) {
    ratingError.value = 'Для оценки нужно войти в аккаунт'
    return
  }
  ratingLoading.value = true
  ratingError.value = ''
  try {
    const payload = {
      value: ratingValue.value,
      user_id: authStore.userId,
      comic_id: comicId.value,
    }
    const res = await fetch(`${API_URL}/comm/${comicId.value}/rate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(payload)
    })
    if (!res.ok) throw new Error(`Ошибка отправки рейтинга: ${res.status}`)
    alert('Оценка отправлена')
  } catch (err) {
    ratingError.value = err.message || 'Ошибка отправки рейтинга'
  } finally {
    ratingLoading.value = false
  }
}

const startReading = () => {
  if (volumes.value.length === 0) return
  const firstVolume = volumes.value[0]
  if (!firstVolume.chapters || firstVolume.chapters.length === 0) return
  const firstChapter = sortedChapters(firstVolume.chapters)[0]
  if (!firstChapter) return

  router.push(`/comic/${comicId.value}/chapter/${firstChapter.id}/page/1`)
}

const goToReader = (comicId, chapterId) => {
  router.push(`/comic/${comicId}/chapter/${chapterId}/page/1`)
}

// Управление томами и главами
const createVolume = async () => {
  if (!isAdminOrAuthor.value) return
  
  volumeLoading.value = true
  try {
    const res = await fetch(`${API_URL}/create/comics/${comicId.value}/volumes`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Ошибка создания тома')
    }
    
    await fetchComicsById(comicId.value)
  } catch (err) {
    alert(err.message)
  } finally {
    volumeLoading.value = false
  }
}

const createChapter = async (volumeId) => {
  if (!isAdminOrAuthor.value) return
  
  chapterLoading.value = true
  try {
    const title = prompt('Введите название главы (необязательно):') || null
    
    const res = await fetch(`${API_URL}/create/volumes/${volumeId}/chapters`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({ title })
    })
    
    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Ошибка создания главы')
    }
    
    await fetchComicsById(comicId.value)
  } catch (err) {
    alert(err.message)
  } finally {
    chapterLoading.value = false
  }
}

const deleteVolume = async (volumeId) => {
  if (!isAdminOrAuthor.value) return
  if (!confirm('Вы уверены? Все главы в этом томе будут удалены.')) return
  
  deletingVolume.value = volumeId
  try {
    const res = await fetch(`${API_URL}/create/volumes/${volumeId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Ошибка удаления тома')
    }
    
    await fetchComicsById(comicId.value)
  } catch (err) {
    alert(err.message)
  } finally {
    deletingVolume.value = null
  }
}

const deleteChapter = async (chapterId) => {
  if (!isAdminOrAuthor.value) return
  if (!confirm('Вы уверены, что хотите удалить главу?')) return
  
  deletingChapter.value = chapterId
  try {
    const res = await fetch(`${API_URL}/create/chapters/${chapterId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Ошибка удаления главы')
    }
    
    await fetchComicsById(comicId.value)
  } catch (err) {
    alert(err.message)
  } finally {
    deletingChapter.value = null
  }
}

const deleteComic = async () => {
  if (authStore.roleId !== 1) return
  if (!confirm('Вы уверены? Весь комикс будет полностью удален.')) return
  
  deletingComic.value = true
  try {
    const res = await fetch(`${API_URL}/comic/comics/${comicId.value}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Ошибка удаления комикса')
    }
    
    router.push('/')
  } catch (err) {
    alert(err.message)
  } finally {
    deletingComic.value = false
  }
}

// Загрузка страниц
const selectChapterForUpload = (chapterId) => {
  selectedChapterForUpload.value = 
    selectedChapterForUpload.value === chapterId ? null : chapterId
}

const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

const handleFileUpload = async (event) => {
  if (!selectedChapterForUpload.value) return
  
  const files = event.target.files
  if (!files.length) return
  
  uploadingPages.value = true
  uploadError.value = ''
  
  try {
    const formData = new FormData()
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i])
    }
    
    const res = await fetch(`${API_URL}/create/chapters/${selectedChapterForUpload.value}/pages`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      },
      body: formData
    })
    
    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Ошибка загрузки страниц')
    }
    
    alert(`Успешно загружено ${files.length} страниц`)
    await fetchComicsById(comicId.value)
  } catch (err) {
    uploadError.value = err.message
  } finally {
    uploadingPages.value = false
    event.target.value = '' // Сброс input
  }
}

const emptyComic = () => ({
  id: 0,
  title: 'Загрузка...',
  desc: '',
  user: { nick: '' },
  date_of_out: '',
  average_rating: 0,
  genres: [],
  img: '',
  volumes: [],
  chaptersCount: 0
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const d = new Date(dateString)
  return d.toLocaleDateString('ru-RU')
}

onMounted(async () => {
  const id = +route.params.id || 0
  await fetchComicsById(id)
  await checkFavoriteStatus()
  await fetchComments()
})

watch(() => route.params.id, async (newId) => {
  const id = +newId || 0
  await fetchComicsById(id)
  await checkFavoriteStatus()
  comments.value = []
  newComment.value = ''
  ratingValue.value = 5
  selectedChapterForUpload.value = null
  await fetchComments()
})
</script>

<style scoped>
select {
  background-color: #1f1f1f;
  color: white;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

input[type="file"] {
  display: none;
}
</style>