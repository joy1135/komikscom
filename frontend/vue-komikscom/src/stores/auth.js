import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    nickname: 'Вход',
    isLoggedIn: false
  }),
  actions: {
    initAuthState() {
      try {
        const token = localStorage.getItem('access_token')
        if (token) {
          const decoded = jwtDecode(token)
          this.nickname = decoded.nick || 'Пользователь'
          this.isLoggedIn = true
        } else {
          this.resetAuthState()
        }
      } catch (error) {
        console.error('Ошибка декодирования токена:', error)
        this.resetAuthState()
      }
    },
    login(token) {
      localStorage.setItem('access_token', token)
      const decoded = jwtDecode(token)
      this.nickname = decoded.nick || 'Пользователь'
      this.isLoggedIn = true
    },
    logout() {
      localStorage.removeItem('access_token')
      this.resetAuthState()
    },
    resetAuthState() {
      this.nickname = 'Вход'
      this.isLoggedIn = false
    }
  }
})