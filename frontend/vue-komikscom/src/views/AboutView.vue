<template>
  
  <div class="main-page">


    <div class="top-releases">
      <div v-for="item in newReleases" :key="item.id" class="cover">
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
          <div class="author">{{ item.author }}</div>
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
      <div v-for="author in newAuthors" :key="author.nickname" class="author-card">
        <img :src="author.avatar_url" alt="Avatar" />
        <div class="nick">{{ author.nickname }}</div>
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
import HelloWorld from '../components/HelloWorld.vue'
import { ref, onMounted } from 'vue'

// const newReleases = ref([]);
// const banner = ref(null);
// const newAuthors = ref([]);
const newReleases = ref([
  {
    id: 1,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 1',
    author: 'Author 1'
  },
  {
    id: 2,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 2',
    author: 'Author 2'
  },
  {
    id: 3,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 3',
    author: 'Author 3'
  },
  {
    id: 1,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 1',
    author: 'Author 1'
  },
  {
    id: 2,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 2',
    author: 'Author 2'
  },
  {
    id: 3,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 3',
    author: 'Author 3'
  },
  {
    id: 1,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 1',
    author: 'Author 1'
  },
  {
    id: 2,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 2',
    author: 'Author 2'
  },
  {
    id: 3,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 3',
    author: 'Author 3'
  },
  {
    id: 1,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 1',
    author: 'Author 1'
  },
  {
    id: 2,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 2',
    author: 'Author 2'
  },
  {
    id: 3,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 3',
    author: 'Author 3'
  },
  {
    id: 1,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 1',
    author: 'Author 1'
  },
  {
    id: 2,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 2',
    author: 'Author 2'
  },
  {
    id: 3,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 3',
    author: 'Author 3'
  },
  {
    id: 1,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 1',
    author: 'Author 1'
  },
  {
    id: 2,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 2',
    author: 'Author 2'
  },
  {
    id: 3,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 3',
    author: 'Author 3'
  },
  {
    id: 1,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 1',
    author: 'Author 1'
  },
  {
    id: 2,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 2',
    author: 'Author 2'
  },
  {
    id: 3,
    cover_url: 'https://dummyimage.com/100x150',
    title: 'New Book 3',
    author: 'Author 3'
  },
]);

const banner = ref({
  link: '#',
  image_url: 'https://dummyimage.com/2000x280'
});

const newAuthors = ref([
  {
    nickname: 'author_1',
    avatar_url: 'https://dummyimage.com/80'
  },
  {
    nickname: 'author_2',
    avatar_url: 'https://dummyimage.com/80'
  },
  {
    nickname: 'author_1',
    avatar_url: 'https://dummyimage.com/80'
  },
  {
    nickname: 'author_2',
    avatar_url: 'https://dummyimage.com/80'
  },
  {
    nickname: 'author_1',
    avatar_url: 'https://dummyimage.com/80'
  },
  {
    nickname: 'author_2',
    avatar_url: 'https://dummyimage.com/80'
  }
]);

onMounted(async () => {
  try {
    // Только если API действительно доступно и работает, раскомментируйте:
    // const response = await fetch(`${import.meta.env.VITE_API_URL}/main`);
    // const data = await response.json();
    
    // Пример загрузки данных, если API доступно
    // newReleases.value = data.new_releases;
    // banner.value = data.banner;
    // newAuthors.value = data.new_authors;
    
    console.log('Фейковые данные загружены');
  } catch (error) {
    console.error('Ошибка запроса:', error);
  }
});
</script>

