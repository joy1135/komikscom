<script setup>
</script>

<template>
<header class="header">
  <div class="logo">
    <div class="logo-star">★</div>
  </div>
  <nav>
    <div>Каталог</div>
    <div>Любимое</div>
  </nav>
  <div class="search-bar">
    <input type="text" placeholder="Поиск">
  </div>
  <nav>
    <div>Вход</div>
  </nav>
</header>
</template>

<style>
.header {
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
</style>
