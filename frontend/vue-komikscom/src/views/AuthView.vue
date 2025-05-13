<template>
  <div class="min-h-screen flex items-center justify-center bg-neutral-900 text-white p-4">
    <div class="bg-black p-8 rounded-xl shadow-md w-full max-w-md space-y-6">
      <h1 class="text-3xl font-bold text-center">Вход / Регистрация</h1>

      <div class="space-y-4">
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

      <div class="flex justify-between">
        <button
          @click="login"
          class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded w-[48%]"
        >
          Войти
        </button>
        <button
          @click="register"
          class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded w-[48%]"
        >
          Регистрация
        </button>
      </div>

      <div v-if="message" class="text-sm text-center text-red-400 mt-2">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const message = ref('')

const login = () => {
  if (!email.value || !password.value) {
    message.value = 'Пожалуйста, заполните все поля.'
    return
  }
  message.value = 'Успешный вход (заглушка)'
}

const register = () => {
  if (!email.value || !password.value) {
    message.value = 'Пожалуйста, заполните все поля.'
    return
  }
  message.value = 'Успешная регистрация (заглушка)'
}
</script>
