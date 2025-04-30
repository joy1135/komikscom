<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import { ref, onMounted } from 'vue'
onMounted(() => {
 
})
</script>

<template>
  <HelloWorld></HelloWorld>
  <RouterView></RouterView>
</template>

<style scoped>
p { 
  color: white;
}
</style>

<style>
body {
  background-color: #181818;
}
</style>
