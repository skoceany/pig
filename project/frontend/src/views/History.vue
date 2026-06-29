<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-800">诊断历史记录</h2>
    </div>

    <div v-if="loading" class="flex justify-center py-12">
      <el-spinner />
    </div>

    <div v-else-if="historyData.records.length === 0" class="text-center py-12">
      <p class="text-gray-500">暂无诊断记录</p>
      <router-link to="/" class="text-primary hover:underline mt-4 inline-block">
        去诊断
      </router-link>
    </div>

    <div v-else>
      <div class="space-y-4">
        <HistoryItem 
          v-for="record in historyData.records" 
          :key="record.id"
          :record="record"
          @delete="handleDelete"
        />
      </div>

      <div class="mt-6 flex justify-center">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="historyData.total"
          @current-change="loadHistory"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HistoryItem from '../components/HistoryItem.vue'
import { diagnosisApi } from '../api/diagnosis'

const historyData = ref({ records: [], total: 0 })
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)

const loadHistory = async () => {
  loading.value = true
  try {
    const response = await diagnosisApi.getHistory({
      page: currentPage.value,
      size: pageSize.value
    })
    historyData.value = response.data.data
  } catch (error) {
    console.error('获取历史记录失败:', error)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (recordId) => {
  try {
    await diagnosisApi.deleteHistory(recordId)
    loadHistory()
  } catch (error) {
    console.error('删除记录失败:', error)
  }
}

onMounted(() => {
  loadHistory()
})
</script>