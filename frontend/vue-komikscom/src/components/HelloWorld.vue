<script setup>
import { RouterLink,useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  authStore.initAuthState()
})

const logout = () => {
  authStore.logout()
  router.push('/')
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
        <div>Любимое</div>
      </nav>
      <div class="search-bar">
        <input type="text" placeholder="Поиск">
      </div>
      <nav class="auth-nav">
        <template v-if="authStore.isLoggedIn">
          <div class="user-info">
            <span>{{ authStore.nickname }}</span>
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
.header{
  background-color: #1c1c1c;
  max-width: 100%;
}
.header-container {
  margin-left: auto;
  margin-right:auto;
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
.auth-nav {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
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
  .user-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .logout-button {
    padding: 3px 8px;
  }
}
</style>
