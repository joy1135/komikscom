<template>
  <div class="reader-container p-4 max-w-4xl mx-auto">
    <header class="flex flex-col md:flex-row justify-between items-center mb-4 gap-4">
      <div class="text-lg font-bold">
        Том {{ store.currentVolumeNumber }}, Глава {{ store.currentChapterNumber }}
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
              v-for="chap in store.allChapters"
              :key="chap.id"
              :value="chap.id"
            >
              Том {{ chap.volume_number }} - Глава {{ chap.number }} {{ chap.title || '' }}
            </option>
          </select>
        </div>

        <div class="flex gap-2 items-center" v-if="store.sortedPages.length">
          <!-- Предыдущая страница/глава -->
          <router-link 
            v-if="previousPageLink"
            :to="previousPageLink"
            custom
            v-slot="{ navigate, isExactActive }"
          >
            <button
              class="nav-button"
              @click="navigate"
              :disabled="isExactActive"
              title="Предыдущая страница"
            >
              &lt;
            </button>
          </router-link>
          <button
            v-else
            class="nav-button"
            disabled
            title="Предыдущая страница"
          >
            &lt;
          </button>
          
          <!-- Селектор страницы -->
          <select 
            id="pageSelect" 
            v-model.number="store.pageNumber" 
            @change="onPageChange" 
            class="p-1 border rounded bg-gray-800 text-white"
          >
            <option v-for="page in store.sortedPages" :key="page.id" :value="page.number">
              {{ page.number }}
            </option>
          </select>
          
          <!-- Следующая страница/глава -->
          <router-link 
            v-if="nextPageLink"
            :to="nextPageLink"
            custom
            v-slot="{ navigate, isExactActive }"
          >
            <button
              class="nav-button"
              @click="navigate"
              :disabled="isExactActive"
              title="Следующая страница"
            >
              &gt;
            </button>
          </router-link>
          <button
            v-else
            class="nav-button"
            disabled
            title="Следующая страница"
          >
            &gt;
          </button>
        </div>
      </div>
    </header>

    <main class="page-image-wrapper border rounded overflow-hidden">
      <img
        v-if="store.currentPage && store.currentPage.image_url"
        :src="getImageUrl(store.currentPage.image_url)"
        :alt="'Страница ' + store.currentPage.number"
        class="mx-auto max-w-full max-h-[80vh]"
        @error="handleImageError"
      />
      <div v-else class="text-center p-10 text-gray-500">
        <div v-if="store.loading">Загрузка страницы...</div>
        <div v-else-if="store.imageError">Ошибка загрузки изображения</div>
        <div v-else>Страница не найдена</div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReaderStore } from '@/stores/store'

const API_URL = import.meta.env.VITE_API_URL 
const API_BASE_URL = import.meta.env.VITE_API_URL1 

const route = useRoute()
const router = useRouter()
const store = useReaderStore()

// Инициализация из параметров маршрута
store.comicId = route.params.comic_id
store.chapterId = Number(route.params.chapter_id)
store.pageNumber = Number(route.params.page_number) || 1

const selectedChapterId = ref(store.chapterId)

// Формируем полный URL изображения
const getImageUrl = (imgPath) => {
  if (!imgPath) return '';
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) return imgPath;
  if (imgPath.startsWith('//')) return window.location.protocol + imgPath;
  return `${API_BASE_URL}/${imgPath}`;
};

const handleImageError = (e) => {
  console.error('Ошибка загрузки изображения:', e);
  store.imageError = true;
};

// Вычисляемые свойства для навигационных ссылок
const previousPageLink = computed(() => {
  if (!store.isFirstPage) {
    const sorted = store.sortedPages
    const idx = sorted.findIndex(p => p.number === store.pageNumber)
    if (idx > 0) {
      return {
        name: 'reader',
        params: { 
          comic_id: store.comicId, 
          chapter_id: store.chapterId, 
          page_number: sorted[idx - 1].number 
        }
      }
    }
  } else if (store.prevChapter) {
    return {
      name: 'reader',
      params: { 
        comic_id: store.comicId, 
        chapter_id: store.prevChapter.id, 
        page_number: 'last' // Специальный маркер для последней страницы
      }
    }
  }
  return null
})

const nextPageLink = computed(() => {
  if (!store.isLastPage) {
    const sorted = store.sortedPages
    const idx = sorted.findIndex(p => p.number === store.pageNumber)
    if (idx < sorted.length - 1) {
      return {
        name: 'reader',
        params: { 
          comic_id: store.comicId, 
          chapter_id: store.chapterId, 
          page_number: sorted[idx + 1].number 
        }
      }
    }
  } else if (store.nextChapter) {
    return {
      name: 'reader',
      params: { 
        comic_id: store.comicId, 
        chapter_id: store.nextChapter.id, 
        page_number: 1 
      }
    }
  }
  return null
})

// Обработчики UI
function onPageChange() {
  router.push({
    name: 'reader',
    params: { 
      comic_id: store.comicId, 
      chapter_id: store.chapterId, 
      page_number: store.pageNumber 
    }
  })
}

function onChapterChange() {
  store.chapterId = selectedChapterId.value
  router.push({
    name: 'reader',
    params: { 
      comic_id: store.comicId, 
      chapter_id: store.chapterId, 
      page_number: 1 
    }
  })
  fetchChapterData(store.chapterId)
}

// Синхронизация селектора главы
watch(() => store.chapterId, (val) => {
  selectedChapterId.value = val
})

// Обработка навигации с маркером 'last'
async function processPageNavigation(to) {
  // Если запрошена последняя страница
  if (to.params.page_number === 'last') {
    const chapterId = Number(to.params.chapter_id)
    
    // Проверяем, известно ли количество страниц
    const chapter = store.allChapters.find(ch => ch.id === chapterId)
    
    if (chapter?.page_count) {
      // Если известно - используем сохраненное значение
      to.params.page_number = chapter.page_count
    } else {
      // Если неизвестно - загружаем данные главы
      const pageCount = await store.fetchChapterPageCount(chapterId)
      to.params.page_number = pageCount > 0 ? pageCount : 1
    }
  }
  
  return to
}

// Реакция на изменения URL
watch(() => route.params, async (newParams) => {
  const newChapterId = Number(newParams.chapter_id)
  const newPageNumber = newParams.page_number // Может быть числом или 'last'
  
  // Обрабатываем навигацию
  const processedParams = await processPageNavigation({
    params: {
      comic_id: store.comicId,
      chapter_id: newChapterId,
      page_number: newPageNumber
    }
  })
  
  // Обновляем URL если параметры изменились
  if (processedParams.params.page_number !== newPageNumber) {
    router.replace({
      name: 'reader',
      params: {
        comic_id: store.comicId,
        chapter_id: newChapterId,
        page_number: processedParams.params.page_number
      }
    })
    return
  }
  
  // Обновляем состояние хранилища
  if (newChapterId !== store.chapterId) {
    store.chapterId = newChapterId
    await fetchChapterData(store.chapterId)
  }
  
  if (Number(processedParams.params.page_number) )
  {
    store.pageNumber = Number(processedParams.params.page_number)
  }
}, { immediate: true, deep: true })

// Загрузка данных
async function fetchComicData() {
  try {
    const res = await fetch(`${API_URL}/comic/comics/${store.comicId}`)
    if (!res.ok) throw new Error(`Ошибка загрузки комикса: ${res.status}`)
    const data = await res.json()
    
    store.allChapters = []
    data.volumes?.forEach(volume => {
      volume.chapters?.forEach(ch => {
        store.allChapters.push({
          id: ch.id,
          number: ch.number,
          title: ch.title,
          volume_number: volume.number,
          page_count: null // Инициализируем null
        })
      })
    })
  } catch (e) {
    console.error('Ошибка загрузки комикса:', e)
  }
}

async function fetchChapterData(chId) {
  try {
    store.loading = true
    store.imageError = false
    
    const chRes = await fetch(`${API_URL}/comic/chapters/${chId}`)
    if (!chRes.ok) throw new Error(`Ошибка загрузки главы: ${chRes.status}`)
    
    const data = await chRes.json()
    store.pages = data || []
    
    // Обновляем количество страниц для главы
    const chapter = store.allChapters.find(ch => ch.id === chId)
    if (chapter) {
      chapter.page_count = store.pages.length
    }
    
    // Установка корректной страницы
    if (store.pages.length > 0) {
      if (!store.pages.some(p => p.number === store.pageNumber)) {
        store.pageNumber = Math.min(...store.pages.map(p => p.number))
      }
    } else {
      store.pageNumber = 1
    }
  } catch (e) {
    console.error('Ошибка загрузки главы:', e)
    store.pages = []
  } finally {
    store.loading = false
  }
}

// Инициализация компонента
onMounted(async () => {
  if (!store.allChapters.length) {
    await fetchComicData()
  }
  
  await fetchChapterData(store.chapterId)
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