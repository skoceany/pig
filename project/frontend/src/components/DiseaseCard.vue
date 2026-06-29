<template>
  <div class="border border-gray-200 rounded-lg p-4 hover:border-primary hover:shadow-md transition-all cursor-pointer">
    <div class="flex items-center justify-between">
      <span class="text-lg">🐷</span>
      <span class="text-xs text-gray-400">{{ diseaseName }}</span>
    </div>
    <h3 class="font-medium text-gray-800 mt-2">{{ diseaseName }}</h3>
    <p class="text-sm text-gray-500 mt-1">点击查看详情</p>
  </div>
</template>

<script setup>
defineProps({
  diseaseName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['click'])
</script>