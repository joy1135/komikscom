<template>
  <div class="min-h-screen flex items-center justify-center bg-neutral-900 text-white p-4">
    <div class="bg-black p-8 rounded-xl shadow-md w-full max-w-md space-y-6">
      <h1 class="text-3xl font-bold text-center">Вход / Регистрация</h1>

        <div class="space-y-6 max-w-md mx-auto p-4">
    <div class="space-y-4">
      <!-- Поле Nickname (только для регистрации) -->
      <input
        v-if="isRegistering"
        type="text"
        v-model="nickname"
        placeholder="Nickname"
        class="w-full px-4 py-2 rounded bg-neutral-800 text-white focus:outline-none focus:ring-2 focus:ring-red-500 transition-all"
      />
      
      <!-- Общие поля -->
      <input
        type="email"
        v-model="email"
        placeholder="Email"
        class="w-full px-4 py-2 rounded bg-neutral-800 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
      />
      <input
        type="password"
        v-model="password"
        placeholder="Пароль"
        class="w-full px-4 py-2 rounded bg-neutral-800 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
      />
    </div>

    <div class="flex justify-between gap-2">
      <button
        @click="handleLogin"
        class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded flex-1 transition-colors"
      >
        Войти
      </button>
      <button
        @click="handleRegisterClick"
        class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded flex-1 transition-colors"
      >
        {{ isRegistering ? 'Зарегистрироваться' : 'Регистрация' }}
      </button>
    </div>
  </div>

      <div v-if="message" class="text-sm text-center text-red-400 mt-2">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import router from '@/router'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const apiUrl = import.meta.env.VITE_API_URL;
const email = ref('')
const password = ref('')
const message = ref('')
const isRegistering = ref(false)
const nickname = ref('')
const authStore = useAuthStore()
const handleLogin = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/user/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded', // Изменили тип контента
      },
      body: new URLSearchParams({
        username: email.value,
        password: password.value,
      }),
    })
    
     if (response.ok) {
      const data = await response.json()
      authStore.login(data.access_token) // Обновляем состояние
      router.push('/catalogue')
    }
  } catch (error) {
    message.value = error.detail || 'Ошибка входа'
  }
}

const handleRegisterClick = async () => {
  if (!isRegistering.value) {
    isRegistering.value = true
    return
  }

  if (!validateRegistration()) return
  
  try {
    const response = await fetch(`${apiUrl}/user/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
        nick: nickname.value
      })
    })

    if (!response.ok) throw await response.json()

    
    message.value = 'Регистрация прошла успешно!'
    resetForm()
  } catch (error) {
    if (error.detail && Array.isArray(error.detail)) {
      message.value = error.detail
        .map(e => {
          // Определяем поле с ошибкой
          const field = e.loc?.[1] || 'unknown'
          
          
          switch(field) {
            case 'email':
              return `Email: ${getEmailError(e)}`
            
            case 'password':
              return `Пароль: ${getPasswordError(e)}`
            
            case 'nick':
              return `👤 Никнейм: ${e.msg}`
            
            default:
              return `❗ ${e.msg}`
          }
        })
        .join('\n')
    }
  }
}

const getEmailError = (error) => {
  if (error.msg.includes('@-sign')) {
    return 'Некорректный формат email'
  }
  return 'Неизвестная ошибка email'
}

const getPasswordError = (error) => {
  const msg = error.msg.toLowerCase()
  if (msg.includes('заглавную')) return 'Должен содержать заглавные буквы'
  if (msg.includes('символ')) return 'Должен содержать специальные символы'
  if (msg.includes('длина')) return 'Минимальная длина - 8 символов'
  return 'Не соответствует требованиям'
}

const validateRegistration = () => {
  if (!nickname.value.trim()) {
    message.value = 'Пожалуйста, введите Nickname'
    return false
  }
  return true
}

const resetForm = () => {
  isRegistering.value = false
  nickname.value = ''
  email.value = ''
  password.value = ''
}
</script>

