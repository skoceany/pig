<template>
  <div>
    <h3 class="text-lg font-medium text-gray-800 mb-4">诊断结果</h3>
    
    <div v-if="loading" class="flex flex-col items-center justify-center py-12">
      <el-spinner />
      <p class="text-gray-500 mt-4">AI正在分析图片...</p>
    </div>
    
    <div v-else-if="result" class="space-y-4">
      <div :class="['px-4 py-3 rounded-lg font-medium text-lg', result.is_sick ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600']">
        {{ result.is_sick ? '⚠️ 检测到患病' : '✅ 健康' }}
      </div>
      
      <div v-if="result.is_sick" class="space-y-4">
        <div class="bg-gray-50 rounded-lg p-4">
          <p class="text-gray-600">疾病名称：<span class="font-medium text-gray-800">{{ result.disease_name }}</span></p>
          <p class="text-gray-600">置信度：<span class="font-medium text-gray-800">{{ (result.confidence * 100).toFixed(1) }}%</span></p>
        </div>
        
        <div>
          <h4 class="font-medium text-gray-800 mb-2">疾病解读</h4>
          <p class="text-gray-600 bg-gray-50 rounded-lg p-4">{{ result.interpretation }}</p>
        </div>
        
        <div v-if="result.symptoms && result.symptoms.length > 0">
          <h4 class="font-medium text-gray-800 mb-2">主要症状</h4>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="symptom in result.symptoms" 
              :key="symptom"
              class="px-3 py-1 bg-red-50 text-red-600 rounded-full text-sm"
            >
              {{ symptom }}
            </span>
          </div>
        </div>
        
        <div v-if="result.recommendations && result.recommendations.length > 0">
          <h4 class="font-medium text-gray-800 mb-2">建议措施</h4>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="rec in result.recommendations" 
              :key="rec"
              class="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-sm"
            >
              {{ rec }}
            </span>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center py-8">
        <p class="text-gray-600">图片中的猪看起来健康</p>
        <p class="text-gray-500 text-sm mt-2">建议继续保持良好的饲养管理</p>
      </div>
    </div>
    
    <div v-else class="text-center py-12">
      <p class="text-gray-500">请上传图片进行诊断</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  result: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})
</script>