<template>
  <div class="reader-container p-4 max-w-4xl mx-auto">
    <header class="flex flex-col md:flex-row justify-between items-center mb-4 gap-4">
      <div class="text-lg font-bold">
        Том {{ currentVolumeNumber }}, Глава {{ currentChapterNumber }}
      </div>

      <div class="flex flex-wrap gap-2 items-center">
        <div class="flex gap-2 items-center">
          <label for="chapterSelect" class="font-semibold">Глава:</label>
          <select 
            id="chapterSelect" 
            v-model="selectedChapterId" 
            @change="onChapterChange" 
            class="p-1 border rounded bg-gray-800 text-white"
          >
            <option
              v-for="chap in allChapters"
              :key="chap.id"
              :value="chap.id"
            >
              Том {{ chap.volume_number }} - Глава {{ chap.number }} {{ chap.title || '' }}
            </option>
          </select>
        </div>

        <div class="flex gap-2 items-center" v-if="sortedPages.length">
          <button
            class="nav-button"
            @click="goToPreviousPage"
            :disabled="isFirstPage && !prevChapter"
            title="Предыдущая страница"
          >
            &lt;
          </button>
          
          <select 
            id="pageSelect" 
            v-model.number="currentPageNumber" 
            @change="onPageChange" 
            class="p-1 border rounded bg-gray-800 text-white"
          >
            <option v-for="page in sortedPages" :key="page.id" :value="page.number">
              {{ page.number }}
            </option>
          </select>
          
          <button
            class="nav-button"
            @click="goToNextPage"
            :disabled="isLastPage && !nextChapter"
            title="Следующая страница"
          >
            &gt;
          </button>
        </div>
      </div>
    </header>

    <main class="page-image-wrapper border rounded overflow-hidden">
      <img
        v-if="currentPage && currentPage.image_url"
        :src="getImageUrl(currentPage.image_url)"
        :alt="'Страница ' + currentPage.number"
        class="mx-auto max-w-full max-h-[80vh]"
        @error="handleImageError"
      />
      <div v-else class="text-center p-10 text-gray-500">
        <div v-if="loadingPages">Загрузка страницы...</div>
        <div v-else-if="imageError">Ошибка загрузки изображения</div>
        <div v-else>Страница не найдена</div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const API_URL = import.meta.env.VITE_API_URL 
const API_BASE_URL = import.meta.env.VITE_API_URL1 

const route = useRoute()
const router = useRouter()

const comicId = route.params.comic_id
const chapterId = ref(Number(route.params.chapter_id))
const currentPageNumber = ref(Number(route.params.page_number) || 1)

const allChapters = ref([])
const pages = ref([])
const loadingPages = ref(true)
const imageError = ref(false)

// Получаем данные из history.state, если есть
const state = window.history.state || {}

if (state.allChapters) {
  allChapters.value = state.allChapters
}

// Сортируем страницы по номеру
const sortedPages = computed(() => {
  return [...pages.value].sort((a, b) => a.number - b.number)
})

const currentPage = computed(() => {
  return sortedPages.value.find(p => p.number === currentPageNumber.value) || null
})

const currentChapterInfo = computed(() => {
  return allChapters.value.find(ch => ch.id === chapterId.value) || {}
})

const currentChapterNumber = computed(() => currentChapterInfo.value.number || '')
const currentVolumeNumber = computed(() => currentChapterInfo.value.volume_number || '')

// Находим индекс текущей главы
const currentChapterIndex = computed(() => {
  return allChapters.value.findIndex(ch => ch.id === chapterId.value)
})

// Находим следующую главу
const nextChapter = computed(() => {
  if (currentChapterIndex.value >= 0 && currentChapterIndex.value < allChapters.value.length - 1) {
    return allChapters.value[currentChapterIndex.value + 1]
  }
  return null
})

// Находим предыдущую главу
const prevChapter = computed(() => {
  if (currentChapterIndex.value > 0) {
    return allChapters.value[currentChapterIndex.value - 1]
  }
  return null
})

const isFirstPage = computed(() => {
  if (!sortedPages.value.length) return true
  const sorted = sortedPages.value
  const currentIndex = sorted.findIndex(p => p.number === currentPageNumber.value)
  return currentIndex <= 0
})

const isLastPage = computed(() => {
  if (!sortedPages.value.length) return true
  const sorted = sortedPages.value
  const currentIndex = sorted.findIndex(p => p.number === currentPageNumber.value)
  return currentIndex >= sorted.length - 1
})

// Формируем полный URL изображения
const getImageUrl = (imgPath) => {
  if (!imgPath) return '';
  
  // Если путь уже абсолютный
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) {
    return imgPath;
  }
  
  // Если путь начинается с //
  if (imgPath.startsWith('//')) {
    return window.location.protocol + imgPath;
  }
  
  // Относительный путь
  return `${API_BASE_URL}/${imgPath}`;
};

// Обработка ошибок загрузки изображения
const handleImageError = (e) => {
  console.error('Ошибка загрузки изображения:', e);
  imageError.value = true;
};

function updateRoute() {
  router.push({
    name: 'reader',
    params: { 
      comic_id: comicId, 
      chapter_id: chapterId.value, 
      page_number: currentPageNumber.value 
    },
    state: {
      allChapters: allChapters.value,
    }
  })
}

// Навигация на следующую страницу
function goToNextPage() {
  if (!isLastPage.value) {
    // Переход на следующую страницу в текущей главе
    const sorted = sortedPages.value
    const currentIndex = sorted.findIndex(p => p.number === currentPageNumber.value)
    
    if (currentIndex >= 0 && currentIndex < sorted.length - 1) {
      currentPageNumber.value = sorted[currentIndex + 1].number
      updateRoute()
    }
  } else if (nextChapter.value) {
    // Переход на первую страницу следующей главы
    chapterId.value = nextChapter.value.id
    currentPageNumber.value = 1
    fetchChapterData(chapterId.value)
  }
}

// Навигация на предыдущую страницу
function goToPreviousPage() {
  if (!isFirstPage.value) {
    // Переход на предыдущую страницу в текущей главе
    const sorted = sortedPages.value
    const currentIndex = sorted.findIndex(p => p.number === currentPageNumber.value)
    
    if (currentIndex > 0) {
      currentPageNumber.value = sorted[currentIndex - 1].number
      updateRoute()
    }
  } else if (prevChapter.value) {
    // Переход на последнюю страницу предыдущей главы
    chapterId.value = prevChapter.value.id
    currentPageNumber.value = 1
    fetchChapterData(chapterId.value, true)
  }
}

// Обработчики выбора страницы и главы
function onPageChange() {
  updateRoute()
}

function onChapterChange() {
  currentPageNumber.value = 1
  chapterId.value = selectedChapterId.value
  fetchChapterData(chapterId.value)
}

const selectedChapterId = ref(chapterId.value)

watch(chapterId, (val) => {
  selectedChapterId.value = val
})

// Реакция на изменение параметров роута
watch(() => route.params, (newParams) => {
  if (newParams.chapter_id && newParams.chapter_id !== chapterId.value.toString()) {
    chapterId.value = Number(newParams.chapter_id)
    fetchChapterData(chapterId.value)
  }
  
  if (newParams.page_number) {
    currentPageNumber.value = Number(newParams.page_number)
  }
})

// Запрос данных комикса и глав
async function fetchComicData() {
  try {
    const res = await fetch(`${API_URL}/comic/comics/${comicId}`)
    if (!res.ok) throw new Error(`Ошибка загрузки комикса: ${res.status}`)
    const data = await res.json()
    allChapters.value = []
    
    if (data.volumes) {
      data.volumes.forEach(volume => {
        if (volume.chapters && volume.chapters.length) {
          volume.chapters.forEach(ch => {
            allChapters.value.push({
              id: ch.id,
              number: ch.number,
              title: ch.title,
              volume_number: volume.number,
            })
          })
        }
      })
    }
  } catch (e) {
    console.error('Ошибка загрузки комикса:', e)
  }
}

// Запрос страниц главы
async function fetchChapterData(chId, setToLastPage = false) {
  try {
    loadingPages.value = true
    imageError.value = false
    
    const chRes = await fetch(`${API_URL}/comic/chapters/${chId}`)
    if (!chRes.ok) throw new Error(`Ошибка загрузки главы: ${chRes.status}`)
    
    const data = await chRes.json()
    pages.value = data || []
    
    // Если текущая страница не валидна, переходим на первую
    if (pages.value.length > 0) {
      if (setToLastPage) {
        // Установка на последнюю страницу
        currentPageNumber.value = Math.max(...pages.value.map(p => p.number))
      } else {
        const pageNumbers = pages.value.map(p => p.number)
        if (!pageNumbers.includes(currentPageNumber.value)) {
          currentPageNumber.value = Math.min(...pageNumbers)
        }
      }
    } else {
      currentPageNumber.value = 1
    }
    
    // Обновляем маршрут
    updateRoute()
  } catch (e) {
    console.error('Ошибка загрузки главы:', e)
    pages.value = []
  } finally {
    loadingPages.value = false
  }
}

onMounted(async () => {
  if (!allChapters.value.length) {
    await fetchComicData()
  }
  
  await fetchChapterData(chapterId.value)
})
</script>

<style scoped>
.reader-container {
  background: #1a1a1a;
  color: white;
  min-height: 100vh;
}

.page-image-wrapper {
  background: #2d2d2d;
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

select {
  background: #333;
  color: white;
  border: 1px solid #555;
  padding: 5px 10px;
  border-radius: 4px;
  min-width: 60px;
}

.nav-button {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #3a3a3a;
  color: white;
  border: 1px solid #555;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

.nav-button:hover:not(:disabled) {
  background: #4a4a4a;
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.flex-wrap {
  flex-wrap: wrap;
}
</style>