<template>
  <div class="min-h-screen flex flex-col">
    <header class="bg-white shadow-sm">
      <div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <span class="text-2xl">🐷</span>
          <h1 class="text-xl font-bold text-gray-800">猪病诊断智能体</h1>
        </div>
        <nav class="flex items-center space-x-6">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path"
            :class="[
              'text-gray-600 hover:text-primary transition-colors',
              $route.path === item.path ? 'text-primary font-medium' : ''
            ]"
          >
            {{ item.name }}
          </router-link>
        </nav>
      </div>
    </header>
    <main class="flex-1 max-w-6xl mx-auto px-4 py-8 w-full">
      <router-view />
    </main>
    <footer class="bg-gray-50 py-4 text-center text-gray-500 text-sm">
      <p>智能养殖猪病诊断智能体 © 2024</p>
    </footer>
  </div>
</template>

<script setup>
const navItems = [
  { name: '诊断', path: '/' },
  { name: '智能对话', path: '/chat' },
  { name: '历史记录', path: '/history' },
  { name: '疾病知识库', path: '/knowledge' },
  { name: '关于', path: '/about' }
]
</script>