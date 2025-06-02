<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const apiUrl = import.meta.env.VITE_API_URL;

const searchQuery = ref('')
const searchResults = ref([])
const showResults = ref(false)
const searchContainerRef = ref(null)

onMounted(() => {
  authStore.initAuthState()
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const handleClickOutside = (event) => {
  if (searchContainerRef.value && 
      !searchContainerRef.value.contains(event.target)) {
    showResults.value = false
  }
}

const logout = () => {
  authStore.logout()
  router.push('/')
}

const searchComics = async () => {
  const query = searchQuery.value.trim()
  if (!query) {
    searchResults.value = []
    showResults.value = false
    return
  }
  
  try {
    const response = await fetch(`${apiUrl}/comic/search?title=${encodeURIComponent(query)}`)
    if (!response.ok) throw new Error('Ошибка поиска')
    
    const data = await response.json()
    searchResults.value = data
    showResults.value = true
  } catch (error) {
    console.error('Ошибка поиска:', error)
    searchResults.value = []
  }
}

const goToComic = (id) => {
  router.push(`/comics/${id}`)
  searchQuery.value = ''
  searchResults.value = []
  showResults.value = false
}
</script>

<template>
  <header class="header">
    <div class="header-container">
      <div class="logo">
        <RouterLink to="/" class="cursor-pointer">
          <div class="logo-star">★</div>
        </RouterLink>
      </div>
      <nav>
        <RouterLink to="/catalogue" class="cursor-pointer">
          Каталог
        </RouterLink>
        <RouterLink to="/favourite" class="cursor-pointer">
          <div>Любимое</div>
        </RouterLink>
      </nav>
      <div class="search-bar" ref="searchContainerRef">
        <div class="search-container">
          <input 
            type="text" 
            placeholder="Поиск"
            v-model="searchQuery"
            @keyup.enter="searchComics"
            @focus="searchComics"
          >
          <div 
            v-if="showResults" 
            class="search-results"
          >
            <div 
              v-for="comic in searchResults" 
              :key="comic.id"
              class="result-item"
              @click="goToComic(comic.id)"
            >
              {{ comic.title }}
            </div>
            <div 
              v-if="searchResults.length === 0" 
              class="result-item not-found"
            >
              Ничего не найдено
            </div>
          </div>
        </div>
      </div>
      <nav class="auth-nav">
        <template v-if="authStore.isLoggedIn">
          <div class="user-info">
            <RouterLink to="/your_profile" class="profile-link">
              {{ authStore.nickname }}
            </RouterLink>
            <button @click="logout" class="logout-button">Выйти</button>
          </div>
        </template>
        <template v-else>
          <RouterLink to="/auth" class="cursor-pointer">
            <div>Вход</div>
          </RouterLink>
        </template>
      </nav>
    </div>
  </header>
</template>

<style>
.header {
  background-color: #1c1c1c;
  max-width: 100%;
  position: relative;
  z-index: 1000;
}

.header-container {
  margin-left: auto;
  margin-right: auto;
  display: flex;
  align-items: center;
  background-color: #1c1c1c;
  padding: 10px 20px;
  color: white;
  max-width: 85vw;
  min-height: 70px;
}

.logo {
  background: red;
  border-radius: 80%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
}

.logo-star {
  color: black;
  font-size: 46px;
}

nav {
  display: flex;
  align-items: center;
  gap: 20px;
  color: white;
  font-weight: bold;
}

.search-bar {
  margin: 0 20px;
  flex-grow: 1;
  position: relative;
}

.search-container {
  position: relative;
}

.search-bar input {
  width: 100%;
  padding: 8px 12px;
  border-radius: 20px;
  border: none;
  background-color: #2a2a2a;
  color: white;
}

.search-bar input::placeholder {
  color: #aaa;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #2a2a2a;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
  margin-top: 5px;
}

.result-item {
  padding: 10px 15px;
  color: #fff;
  cursor: pointer;
  border-bottom: 1px solid #3a3a3a;
  transition: background-color 0.2s;
}

.result-item:hover {
  background-color: #3a3a3a;
}

.result-item:last-child {
  border-bottom: none;
}

.not-found {
  color: #aaa;
  cursor: default;
}

.auth-nav {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile-link {
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 5px 10px;
  border-radius: 4px;
  margin-right: 10px;
}

.profile-link:hover {
  background-color: #3a3a3a;
  text-decoration: underline;
}

.logout-button {
  background: #2a2a2a;
  color: #aaa;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.logout-button:hover {
  background: #3a3a3a;
  color: white;
}

/* Для мобильной адаптации */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    padding: 10px;
  }

  .logo {
    margin-right: 0;
    margin-bottom: 10px;
  }

  nav {
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }

  .auth-nav {
    width: 100%;
    margin-top: 10px;
  }

  .user-info {
    width: 100%;
    justify-content: space-between;
    flex-direction: row;
  }

  .search-bar {
    width: 100%;
    margin: 0;
  }

  .search-bar input {
    width: 100%;
    font-size: 1rem;
  }

  .search-results {
    position: absolute;
    top: calc(100% + 5px);
    left: 0;
    right: 0;
    max-height: 200px;
    font-size: 0.9rem;
  }

  .result-item {
    padding: 8px 12px;
  }

  .profile-link, .logout-button {
    font-size: 0.9rem;
  }
}
</style>