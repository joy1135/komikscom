import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useReaderStore = defineStore('reader', () => {
  // Состояния
  const comicId = ref(null)
  const chapterId = ref(null)
  const pageNumber = ref(1)
  const allChapters = ref([])
  const pages = ref([])
  const loading = ref(false)
  const imageError = ref(false)
  
  // Геттеры
  const sortedPages = computed(() => {
    return [...pages.value].sort((a, b) => a.number - b.number)
  })
  
  const currentPage = computed(() => {
    return sortedPages.value.find(page => page.number === pageNumber.value)
  })
  
  const currentChapter = computed(() => {
    return allChapters.value.find(ch => ch.id === chapterId.value)
  })
  
  const currentVolumeNumber = computed(() => {
    return currentChapter.value?.volume_number || ''
  })
  
  const currentChapterNumber = computed(() => {
    return currentChapter.value?.number || ''
  })
  
  const isFirstPage = computed(() => {
    if (sortedPages.value.length === 0) return true
    return pageNumber.value === sortedPages.value[0].number
  })
  
  const isLastPage = computed(() => {
    if (sortedPages.value.length === 0) return true
    return pageNumber.value === sortedPages.value[sortedPages.value.length - 1].number
  })
  
  const prevChapter = computed(() => {
    const index = allChapters.value.findIndex(ch => ch.id === chapterId.value)
    return index > 0 ? allChapters.value[index - 1] : null
  })
  
  const nextChapter = computed(() => {
    const index = allChapters.value.findIndex(ch => ch.id === chapterId.value)
    return index >= 0 && index < allChapters.value.length - 1 
      ? allChapters.value[index + 1] 
      : null
  })

  // Действия
  async function fetchComicData() {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/comic/comics/${comicId.value}`)
      if (!res.ok) throw new Error(`Failed to load comic: ${res.status}`)
      const data = await res.json()
      
      allChapters.value = []
      data.volumes?.forEach(volume => {
        volume.chapters?.forEach(ch => {
          allChapters.value.push({
            id: ch.id,
            number: ch.number,
            title: ch.title,
            volume_number: volume.number,
            // Новое поле для хранения количества страниц
            page_count: null
          })
        })
      })
    } catch (e) {
      console.error('Comic loading error:', e)
    }
  }
  
  // Новая функция: загрузка данных главы и подсчёт страниц
  async function fetchChapterPageCount(chId) {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/comic/chapters/${chId}`)
      if (!res.ok) throw new Error(`Failed to load chapter: ${res.status}`)
      
      const data = await res.json()
      const pageCount = data?.length || 0
      
      // Обновляем информацию о количестве страниц в главе
      const chapter = allChapters.value.find(ch => ch.id === chId)
      if (chapter) {
        chapter.page_count = pageCount
      }
      
      return pageCount
    } catch (e) {
      console.error('Chapter page count loading error:', e)
      return 0
    }
  }
  
  async function fetchChapterData(chId) {
    try {
      loading.value = true
      imageError.value = false
      
      const res = await fetch(`${import.meta.env.VITE_API_URL}/comic/chapters/${chId}`)
      if (!res.ok) throw new Error(`Failed to load chapter: ${res.status}`)
      
      const data = await res.json()
      pages.value = data || []
      
      // Обновляем количество страниц для текущей главы
      const chapter = allChapters.value.find(ch => ch.id === chId)
      if (chapter) {
        chapter.page_count = pages.value.length
      }
    } catch (e) {
      console.error('Chapter loading error:', e)
      pages.value = []
    } finally {
      loading.value = false
    }
  }

  return {
    // Состояния
    comicId,
    chapterId,
    pageNumber,
    allChapters,
    pages,
    loading,
    imageError,
    
    // Геттеры
    sortedPages,
    currentPage,
    currentVolumeNumber,
    currentChapterNumber,
    isFirstPage,
    isLastPage,
    prevChapter,
    nextChapter,
    
    // Действия
    fetchComicData,
    fetchChapterData,
    fetchChapterPageCount // Новый метод
  }
})