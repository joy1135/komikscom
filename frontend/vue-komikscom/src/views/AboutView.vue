<template>
  <div class="main-page">
    <!-- Top Recommendations -->
    <div class="top-releases">
      <div v-for="item in topReleases" :key="item.id" class="cover">
        <img :src="item.cover_url" alt="Cover" />
      </div>
    </div>

    <div class="main-page-container">
      <h2>Новинки</h2>
      <div class="new-releases">
        <div v-for="item in newReleases" :key="item.id" class="release-item">
          <img :src="item.cover_url" alt="Cover" />
          <div class="info">
            <div>{{ item.title }}</div>
          </div>
        </div>
      </div>
      
      <div v-if="banner" class="banner">
        <a :href="banner.link">
          <img :src="banner.image_url" alt="Banner" />
        </a>
      </div>

      <h2>Новые авторы</h2>
      <div class="new-authors">
        <div v-for="author in newAuthors" :key="author.id" class="author-card">
          <img :src="author.avatar_url || 'https://dummyimage.com/80'" alt="Avatar" />
          <div class="nick">{{ author.nick }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-page {
  background: white;
  padding: 20px;
}
.main-page-container{
  display: flex;
  flex-direction: column;
  margin: auto;
  max-width: 85vw;
}
.top-releases {
  display: flex;
  overflow-x: auto;
  gap: 10px;
}

.top-releases .cover img {
  width: 100px;
  height: 150px;
  object-fit: cover;
}

.new-releases {
  background-color: #1A1A1A;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.release-item {
  width: 100px;
}

.release-item img {
  width: 100px;
  height: 150px;
  object-fit: cover;
}

.info {
  color: rgb(255, 255, 255);
}
.banner{
  margin: auto;
}
.banner img {
  width: 100%;
  border-radius: 10px;
  margin: 20px 0;
}

.new-authors {
  min-width: 85vw;
  margin: auto;
  display: flex;
  gap: 20px;
  background-color: #1A1A1A;
}

.author-card {
  text-align: center;
  
}
.nick{
  color: white;
}
.author-card img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}
</style>
<script setup>
import { ref, onMounted } from 'vue'

const topReleases = ref([]) // Для рекомендаций
const newReleases = ref([]) // Для новинок
const newAuthors = ref([])  // Для новых авторов
const banner = ref(null)
const authorsMap = ref({})  // Для хранения информации об авторах


const fetchData = async () => {
  try {
    // Запрос для топовых рекомендаций
    const topResponse = await fetch(`${import.meta.env.VITE_API_URL}/comic/recomm`)
    topReleases.value = await topResponse.json()
    
    // Запрос для новинок
    const newResponse = await fetch(`${import.meta.env.VITE_API_URL}/comic/new_5`)
    newReleases.value = await newResponse.json()
    
    // Запрос для новых авторов
    const authorsResponse = await fetch(`${import.meta.env.VITE_API_URL}/aftor/new_authors`)
    newAuthors.value = await authorsResponse.json()
    
    
    newAuthors.value.forEach(author => {
      authorsMap.value[author.id] = author
    })
    
    console.log('Данные успешно загружены')
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error)
  }
}


const getAuthorName = (userId) => {
  return authorsMap.value[userId]?.nickname || 'Неизвестный автор'
}

onMounted(fetchData)
</script>