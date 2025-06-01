<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
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
}
</style>