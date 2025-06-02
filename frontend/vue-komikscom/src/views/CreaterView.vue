<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const apiUrl = import.meta.env.VITE_API_URL

// Данные формы
const title = ref('')
const desc = ref('')
const posterFile = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')

// Обработка выбора файла
const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Проверка типа файла
    if (!file.type.match('image.*')) {
      errorMessage.value = 'Пожалуйста, выберите изображение (JPEG, PNG, GIF)'
      return
    }
    
    // Проверка размера файла (максимум 5MB)
    if (file.size > 5 * 1024 * 1024) {
      errorMessage.value = 'Размер файла не должен превышать 5MB'
      return
    }
    
    posterFile.value = file
    errorMessage.value = ''
  }
}

// Отправка формы
const submitForm = async () => {
  // Валидация
  if (!title.value.trim()) {
    errorMessage.value = 'Название комикса обязательно'
    return
  }
  
  if (!posterFile.value) {
    errorMessage.value = 'Постер обязателен'
    return
  }
  
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const formData = new FormData()
    formData.append('title', title.value)
    if (desc.value) formData.append('desc', desc.value)
    formData.append('poster', posterFile.value)
    
    const response = await fetch(`${apiUrl}/create/comics/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: formData
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Ошибка создания комикса')
    }
    
    const comicData = await response.json()
    router.push(`/comics/${comicData.id}`)
    
  } catch (error) {
    console.error('Ошибка создания комикса:', error)
    errorMessage.value = error.message || 'Произошла ошибка при создании комикса'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="create-comic-container">
    <h1 class="create-comic-title">Создать новый комикс</h1>
    
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    
    <form @submit.prevent="submitForm" class="comic-form">
      <div class="form-group">
        <label for="title">Название комикса *</label>
        <input 
          type="text" 
          id="title" 
          v-model="title" 
          placeholder="Введите название комикса"
          maxlength="100"
        >
      </div>
      
      <div class="form-group">
        <label for="desc">Описание</label>
        <textarea 
          id="desc" 
          v-model="desc" 
          placeholder="Краткое описание комикса"
          rows="4"
          maxlength="500"
        ></textarea>
        <div class="char-counter">{{ desc.length }}/500</div>
      </div>
      
      <div class="form-group">
        <label for="poster">Постер *</label>
        <div class="file-upload">
          <input 
            type="file" 
            id="poster" 
            accept="image/*"
            @change="handleFileChange"
          >
          <label for="poster" class="file-upload-label">
            <span v-if="posterFile">{{ posterFile.name }}</span>
            <span v-else>Выберите файл</span>
          </label>
          <div class="file-hint">JPG, PNG или GIF (макс. 5MB)</div>
        </div>
      </div>
      
      <div class="form-actions">
        <button 
          type="submit" 
          class="submit-button"
          :disabled="isLoading"
        >
          <span v-if="isLoading">Создание...</span>
          <span v-else>Создать комикс</span>
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.create-comic-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 25px;
  background-color: #1c1c1c;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.create-comic-title {
  text-align: center;
  color: #fff;
  margin-bottom: 30px;
  font-size: 32px;
  position: relative;
  padding-bottom: 15px;
}

.create-comic-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: linear-gradient(90deg, #ff6b6b, #4fc3f7);
  border-radius: 3px;
}

.error-message {
  background-color: #ff6b6b;
  color: white;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 25px;
  text-align: center;
  font-weight: bold;
}

.comic-form {
  background-color: #2a2a2a;
  padding: 30px;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #ff6b6b;
  font-size: 18px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 15px;
  border-radius: 6px;
  border: 1px solid #444;
  background-color: #333;
  color: white;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #ff6b6b;
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 107, 107, 0.2);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.char-counter {
  text-align: right;
  font-size: 14px;
  color: #aaa;
  margin-top: 5px;
}

.file-upload {
  position: relative;
}

.file-upload input[type="file"] {
  display: none;
}

.file-upload-label {
  display: block;
  padding: 12px 15px;
  background-color: #333;
  border: 1px solid #444;
  border-radius: 6px;
  color: #aaa;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.file-upload-label:hover {
  background-color: #3a3a3a;
  border-color: #ff6b6b;
}

.file-hint {
  font-size: 14px;
  color: #aaa;
  margin-top: 8px;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.submit-button {
  background: linear-gradient(135deg, red, #ff5252);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 14px 35px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 200px;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
}

.submit-button:active:not(:disabled) {
  transform: translateY(0);
}

.submit-button:disabled {
  background: #555;
  cursor: not-allowed;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .create-comic-container {
    margin: 20px;
    padding: 20px;
  }
  
  .comic-form {
    padding: 20px;
  }
  
  .submit-button {
    width: 100%;
    padding: 16px;
  }
}
</style>