<template>
  <div class="border border-gray-200 rounded-lg p-4">
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <div class="flex items-center space-x-2">
          <span :class="['px-2 py-1 rounded text-sm font-medium', record.is_sick ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600']">
            {{ record.is_sick ? '患病' : '健康' }}
          </span>
          <span class="text-gray-800 font-medium">{{ record.disease_name }}</span>
          <span class="text-gray-500 text-sm">置信度: {{ (record.confidence * 100).toFixed(1) }}%</span>
        </div>
        <p class="text-gray-600 text-sm mt-2 line-clamp-2">{{ record.interpretation }}</p>
        <p class="text-gray-400 text-xs mt-2">{{ record.created_at }}</p>
      </div>
      <el-button type="danger" size="small" @click="handleDelete">
        删除
      </el-button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  record: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['delete'])

const handleDelete = () => {
  emit('delete', props.record.id)
}
</script>