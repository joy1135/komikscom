<template>
  <div class="main-page">
    <!-- Top Recommendations -->
    <div class="top-releases">
      <div v-for="item in topReleases" :key="item.id" class="cover">
        <img 
          :src="getFullImageUrl(item.img)" 
          @error="handleImageError"
          alt="Cover" 
        />
      </div>
    </div>

    <div class="main-page-container">
      <h2>Новинки</h2>
      <div class="new-releases">
        <div v-for="item in newReleases" :key="item.id" class="release-item">
          <img 
            :src="getFullImageUrl(item.img)" 
            @error="handleImageError"
            alt="Cover" 
          />
          <div class="info">
            <div>{{ item.title }}</div>
            <div class="author">{{ getAuthorName(item.userID) }}</div>
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
          <img 
            :src="getFullImageUrl(author.avatar_url)" 
            @error="handleAvatarError"
            alt="Avatar" 
          />
          <div class="nick">{{ author.nickname }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Стили без изменений */
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

const API_BASE_URL = import.meta.env.VITE_API_URL1;

const API_URL = import.meta.env.VITE_API_URL;

const topReleases = ref([]);
const newReleases = ref([]);
const newAuthors = ref([]);
const banner = ref(null);
const authorsMap = ref({});

const getFullImageUrl = (imgPath) => {
  if (!imgPath) return '';
  
  // Если путь уже является абсолютным URL
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) {
    return imgPath;
  }
  
  // Если путь начинается с двойного слеша (//example.com)
  if (imgPath.startsWith('//')) {
    return window.location.protocol + imgPath;
  }
  
  // Если путь абсолютный (начинается с /)
  if (imgPath.startsWith('/')) {
    return API_BASE_URL + imgPath;
  }
  
  // Относительный путь
  return API_BASE_URL +"/"+ imgPath;
};

const handleImageError = (event) => {
  console.error('Ошибка загрузки изображения:', event.target.src);
  event.target.src = 'https://dummyimage.com/100x150/000/fff&text=Cover+Error';
};

const handleAvatarError = (event) => {
  console.error('Ошибка загрузки аватара:', event.target.src);
  event.target.src = 'https://dummyimage.com/80/000/fff&text=Avatar+Error';
};

const fetchData = async () => {
  try {
    // Запросы к API
    const [topRes, newRes, authorsRes] = await Promise.all([
      fetch(`${API_URL}/comic/recomm`),
      fetch(`${API_URL}/comic/new_5`),
      fetch(`${API_URL}/aftor/new_authors`)
    ]);
    
    topReleases.value = await topRes.json();
    newReleases.value = await newRes.json();
    newAuthors.value = await authorsRes.json();
    
    // Логирование для отладки
    console.log("Top Releases:", topReleases.value);
    console.log("New Releases:", newReleases.value);
    console.log("New Authors:", newAuthors.value);
    
    // Создаем карту авторов
    newAuthors.value.forEach(author => {
      authorsMap.value[author.id] = author;
    });
    
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
}

const getAuthorName = (userId) => {
  return authorsMap.value[userId]?.nickname || 'Неизвестный автор';
}

onMounted(fetchData);
</script>