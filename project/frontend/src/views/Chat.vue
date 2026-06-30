<template>
  <div class="bg-white rounded-lg shadow-sm p-6 h-[600px] flex flex-col">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-bold text-gray-800">智能助手</h2>
      <el-button size="small" @click="clearChat">清空对话</el-button>
    </div>

    <div class="flex-1 overflow-y-auto space-y-4 mb-4">
      <div 
        v-for="(msg, index) in messages" 
        :key="index"
        :class="[
          'flex',
          msg.role === 'user' ? 'justify-end' : 'justify-start'
        ]"
      >
        <div 
          :class="[
            'max-w-[70%] px-4 py-3 rounded-lg',
            msg.role === 'user' 
              ? 'bg-blue-500 text-white rounded-br-none' 
              : 'bg-gray-100 text-gray-800 rounded-bl-none'
          ]"
        >
          <p>{{ msg.content }}</p>
        </div>
      </div>

      <div v-if="loading" class="flex justify-start">
        <div class="bg-gray-100 px-4 py-3 rounded-lg rounded-bl-none">
          <el-spinner size="small" />
        </div>
      </div>
    </div>

    <div class="flex gap-2">
      <el-input 
        v-model="inputMessage" 
        placeholder="输入您的问题..."
        @keyup.enter="sendMessage"
        class="flex-1"
      />
      <el-button type="primary" @click="sendMessage" :disabled="!inputMessage || loading">
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { diagnosisApi } from '../api/diagnosis'

const messages = ref([
  { role: 'assistant', content: '您好！我是猪病诊断智能助手。请问有什么可以帮助您的？' }
])
const inputMessage = ref('')
const loading = ref(false)

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = inputMessage.value.trim()
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  loading.value = true

  try {
    const response = await diagnosisApi.chat(userMessage)
    messages.value.push({ role: 'assistant', content: response.data.data.response })
  } catch (error) {
    console.error('聊天失败:', error)
    messages.value.push({ role: 'assistant', content: '抱歉，我暂时无法回答您的问题。' })
  } finally {
    loading.value = false
  }
}

const clearChat = () => {
  messages.value = [
    { role: 'assistant', content: '您好！我是猪病诊断智能助手。请问有什么可以帮助您的？' }
  ]
}
</script>
