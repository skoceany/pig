<template>
  <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer" @click="triggerUpload" @drop.prevent="handleDrop" @dragover.prevent>
    <input 
      ref="fileInput"
      type="file" 
      accept="image/*" 
      class="hidden"
      @change="handleFileChange"
    />
    
    <div class="space-y-4">
      <div class="text-6xl">📷</div>
      <div>
        <p class="text-lg font-medium text-gray-800">点击或拖拽上传图片</p>
        <p class="text-sm text-gray-500 mt-1">支持 JPG、PNG、BMP 格式，最大 5MB</p>
      </div>
      
      <el-button type="primary" @click.stop="triggerUpload">
        选择文件
      </el-button>
    </div>
    
    <div v-if="uploading" class="mt-4">
      <el-progress :percentage="uploadProgress" />
      <p class="text-sm text-gray-500 mt-2">上传中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['upload', 'error'])
const fileInput = ref(null)
const uploading = ref(false)
const uploadProgress = ref(0)

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    validateFile(file)
  }
}

const handleDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file) {
    validateFile(file)
  }
}

const validateFile = (file) => {
  const types = ['image/jpeg', 'image/png', 'image/bmp']
  if (!types.includes(file.type)) {
    emit('error', '仅支持JPG、PNG、BMP格式')
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    emit('error', '文件大小不能超过5MB')
    return
  }
  emit('upload', file)
}
</script>