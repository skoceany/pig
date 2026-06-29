<template>
  <div class="max-w-4xl mx-auto">
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">智能猪病诊断</h2>
      <p class="text-gray-600">上传猪的照片，AI将为您分析是否患病及具体病症</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="bg-white rounded-lg shadow-sm p-6">
        <ImageUploader @upload="handleUpload" />
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <DiagnosisResult 
          :result="diagnosisResult" 
          :loading="isLoading"
        />
      </div>
    </div>

    <div v-if="uploadedImage" class="mt-8 bg-white rounded-lg shadow-sm p-6">
      <h3 class="text-lg font-medium text-gray-800 mb-4">上传的图片</h3>
      <img 
        :src="uploadedImage" 
        alt="上传的猪照片"
        class="max-w-full h-auto rounded-lg"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ImageUploader from '../components/ImageUploader.vue'
import DiagnosisResult from '../components/DiagnosisResult.vue'
import { diagnosisApi } from '../api/diagnosis'

const diagnosisResult = ref(null)
const isLoading = ref(false)
const uploadedImage = ref(null)

const handleUpload = async (file) => {
  isLoading.value = true
  diagnosisResult.value = null
  
  const formData = new FormData()
  formData.append('image', file)
  
  uploadedImage.value = URL.createObjectURL(file)
  
  try {
    const response = await diagnosisApi.diagnose(formData)
    diagnosisResult.value = response.data.data
  } catch (error) {
    console.error('诊断失败:', error)
    alert('诊断失败，请重试')
  } finally {
    isLoading.value = false
  }
}
</script>