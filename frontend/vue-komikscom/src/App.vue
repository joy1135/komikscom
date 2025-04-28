<script setup>
// import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
import { ref, onMounted } from 'vue'

const res = ref(null)

onMounted(async () => {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/hello`);
  const data = await response.json();
  res.value = data.message;  // например, ожидаем { message: "Hello from FastAPI" }
});
</script>

<template>
  <p>{{ res }}</p>
  
</template>

<style scoped>
p { 
  color: black;
}
</style>
