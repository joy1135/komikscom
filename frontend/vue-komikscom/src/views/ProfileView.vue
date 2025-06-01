<script setup>
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// Вычисляемое свойство для преобразования роли в текст
const userRole = computed(() => {
  if (authStore.role === null || authStore.role === undefined) return 'Недоступно'
  
  switch(authStore.role) {
    case 1: return 'Администратор'
    case 2: return 'Пользователь'
    case 3: return 'Автор'
    default: return `Неизвестная роль (${authStore.role})`
  }
})


const roleStyle = computed(() => {
  switch(authStore.role) {
    case 1: return { color: '#ff6b6b', fontWeight: 'bold' } 
    case 3: return { color: '#4fc3f7' }
    default: return {} 
  }
})

const canCreateComics = computed(() => {
  return authStore.role === 1 || authStore.role === 3
})

const navigateToCreateComic = () => {
  router.push('/create-comic')
}
</script>

<template>
  <div class="profile-container">
    <h1 class="profile-title">Ваш профиль</h1>
    
    <div class="profile-info">
      <div class="info-item">
        <span class="info-label">Никнейм:</span>
        <span class="info-value">{{ authStore.nickname }}</span>
      </div>
      
      <div class="info-item" v-if="authStore.email">
        <span class="info-label">Почта:</span>
        <span class="info-value">{{ authStore.email }}</span>
      </div>
      
      <div class="info-item">
        <span class="info-label">ID пользователя:</span>
        <span class="info-value">{{ authStore.userId || 'Недоступно' }}</span>
      </div>
      
      <div class="info-item">
        <span class="info-label">Ваша роль:</span>
        <span class="info-value" :style="roleStyle">{{ userRole }}</span>
      </div>
    </div>

    <div class="action-buttons" v-if="canCreateComics">
      <button class="create-comic-button" @click="navigateToCreateComic">
        Создать комикс
      </button>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  background-color: #1c1c1c;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  position: relative;
}

.profile-title {
  text-align: center;
  color: #fff;
  margin-bottom: 30px;
  font-size: 28px;
}

.profile-info {
  background-color: #2a2a2a;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #3a3a3a;
}

.info-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.info-label {
  font-weight: bold;
  color: #ff6b6b;
  min-width: 150px;
}

.info-value {
  color: #fff;
  flex-grow: 1;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 25px;
}

.create-comic-button {
  background-color: red;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 12px 25px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.create-comic-button:hover {
  background-color: #ff5252;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
}

.create-comic-button:active {
  transform: translateY(0);
  box-shadow: none;
}

@media (max-width: 768px) {
  .profile-container {
    margin: 20px;
    padding: 15px;
  }
  
  .info-item {
    flex-direction: column;
  }
  
  .info-label {
    margin-bottom: 5px;
  }
  
  .create-comic-button {
    width: 100%;
    padding: 15px;
    font-size: 18px;
  }
}
</style>