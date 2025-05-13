<template>
  <div class="min-h-screen bg-white text-white flex">
    <!-- Каталог -->
    <div class="w-3/4 bg-neutral-900 p-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Каталог</h2>
        <button class="bg-gray-700 text-white px-4 py-1 rounded">По популярности</button>
      </div>

      <input
        type="text"
        placeholder="Поиск по названию"
        class="w-full p-2 rounded bg-neutral-800 text-white "
      />

      <div class="grid grid-cols-5 gap-4 mt-4">
        <div
          v-for="n in 15"
          :key="n"
          class="bg-black p-2 rounded shadow-md flex flex-col items-center"
        >
          <img
            src="https://dummyimage.com/100x150"
            alt="cover"
            class="w-24 h-32 object-cover rounded"
          />
          <div class="mt-2 text-center">
            <div class="font-bold text-sm">Название</div>
            <div class="text-xs text-gray-400">Автор</div>
          </div>
        </div>
      </div>
    </div>

   
    <div class="w-1/4 bg-black p-4">
      <h3 class="text-lg font-semibold mb-2">Жанры</h3>
      <div class="flex flex-col space-y-1 mb-4">
        <label><input type="checkbox" /> Спорт</label>
        <label><input type="checkbox" /> Детектив</label>
        <label><input type="checkbox" /> Боевик</label>
      </div>

      <h3 class="text-lg font-semibold mb-2">Оценка</h3>
      <div class="flex flex-col space-y-1">
        <label v-for="score in 10" :key="score">
          <input type="checkbox" /> {{ score }}
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>

</script>
