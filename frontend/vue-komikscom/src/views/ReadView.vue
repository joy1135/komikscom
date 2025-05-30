<template>
  <div class="reader-container p-4 max-w-4xl mx-auto">
    <header class="flex flex-col md:flex-row justify-between items-center mb-4 gap-4">
      <div class="text-lg font-bold">
        Том {{ currentVolumeNumber }}, Глава {{ currentChapterNumber }}
      </div>

      <div class="flex gap-2 items-center">
        <label for="chapterSelect" class="font-semibold">Выбор главы:</label>
        <select id="chapterSelect" v-model="selectedChapterId" @change="onChapterChange" class="p-1 border rounded">
          <option
            v-for="chap in allChapters"
            :key="chap.id"
            :value="chap.id"
          >
            Том {{ chap.volume_number }} - Глава {{ chap.number }} {{ chap.title || '' }}
          </option>
        </select>
      </div>

      <div class="flex gap-2 items-center" v-if="pages.length">
        <label for="pageSelect" class="font-semibold">Выбор страницы:</label>
        <select id="pageSelect" v-model.number="pageNumber" @change="onPageChange" class="p-1 border rounded">
          <option v-for="page in pages" :key="page.id" :value="page.number">
            {{ page.number }}
          </option>
        </select>
      </div>

      <button
        class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
        @click="goToNextPage"
        :disabled="isLastPage"
      >
        Следующая страница →
      </button>
    </header>

    <main class="page-image-wrapper border rounded overflow-hidden">
      <img
        v-if="currentPage"
        :src="imageBaseUrl + '/' + currentPage.image_url"
        :alt="'Страница ' + currentPage.number"
        class="mx-auto max-w-full max-h-[80vh]"
      />
      <div v-else class="text-center p-10 text-gray-500">Загрузка страницы...</div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const API_URL = import.meta.env.VITE_API_URL || ''

const route = useRoute()
const router = useRouter()

const comicId = route.params.comic_id
const chapterId = ref(route.params.chapter_id)
const pageNumber = ref(Number(route.params.page_number) || 1)

const chapterData = ref(null)
const allChapters = ref([])

const imageBaseUrl = API_URL

// Получаем данные из history.state, если есть
const state = window.history.state || {}

if(state.chapterData && state.allChapters) {
  chapterData.value = state.chapterData
  allChapters.value = state.allChapters
} 

function updateRouteWithState(chId, pNum) {
  router.push({
    name: 'reader',
    params: { comic_id: comicId, chapter_id: chId, page_number: pNum },
    state: {
      chapterData: chapterData.value,
      allChapters: allChapters.value,
    }
  })
}

// Преобразуем номера страниц в числа и сортируем
const pages = computed(() => {
  if (!chapterData.value?.pages) return []
  return [...chapterData.value.pages]
    .map(p => ({ ...p, number: Number(p.number) }))
    .sort((a, b) => a.number - b.number)
})

const currentPage = computed(() => {
  return pages.value.find(p => p.number === pageNumber.value) || null
})

const currentChapterNumber = computed(() => chapterData.value?.number || '')
const currentVolumeNumber = computed(() => chapterData.value?.volume_number || '')

const isLastPage = computed(() => {
  if (!pages.value.length) return true
  const maxPageNumber = Math.max(...pages.value.map(p => p.number))
  return pageNumber.value >= maxPageNumber
})

// Навигация на следующую страницу
function goToNextPage() {
  if (isLastPage.value) return
  pageNumber.value++
  updateRouteWithState(chapterId.value, pageNumber.value)
}

// Обработчики выбора страницы и главы
function onPageChange() {
  updateRouteWithState(chapterId.value, pageNumber.value)
}

function onChapterChange() {
  pageNumber.value = 1
  chapterId.value = selectedChapterId.value || chapterId.value
  fetchChapterData(chapterId.value)
  updateRouteWithState(chapterId.value, pageNumber.value)
}

const selectedChapterId = ref(chapterId.value)

watch(chapterId, (val) => {
  selectedChapterId.value = val
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
        volume.chapters.forEach(ch => {
          allChapters.value.push({
            id: ch.id,
            number: ch.number,
            title: ch.title,
            volume_number: volume.number,
          })
        })
      })
      allChapters.value.sort((a, b) => {
        if (a.volume_number !== b.volume_number) return a.volume_number - b.volume_number
        return a.number - b.number
      })
    }
  } catch (e) {
    console.error(e)
  }
}

// Запрос данных конкретной главы
async function fetchChapterData(chId) {
  try {
    const chRes = await fetch(`${API_URL}/comic/chapters/${chId}`)
    if (!chRes.ok) throw new Error(`Ошибка загрузки главы: ${chRes.status}`)
    chapterData.value = await chRes.json()
  } catch (e) {
    console.error(e)
  }
}

onMounted(async () => {
  if (!allChapters.value.length) {
    await fetchComicData()
  }
  if (!chapterData.value) {
    await fetchChapterData(chapterId.value)
  }
})
</script>

<style scoped>
.reader-container {
  background: #1a1a1a;
  color: white;
  min-height: 100vh;
}
.page-image-wrapper img {
  display: block;
}
</style>
