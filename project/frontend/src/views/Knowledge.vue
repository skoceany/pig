<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-800">疾病知识库</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <DiseaseCard 
        v-for="disease in diseases" 
        :key="disease"
        :disease-name="disease"
        @click="showDiseaseDetail(disease)"
      />
    </div>

    <el-dialog 
      v-model="dialogVisible" 
      :title="selectedDisease?.disease_name"
      width="600px"
    >
      <div v-if="selectedDisease" class="space-y-4">
        <div>
          <h3 class="font-medium text-gray-800 mb-2">疾病概述</h3>
          <p class="text-gray-600">{{ selectedDisease.description }}</p>
        </div>
        <div>
          <h3 class="font-medium text-gray-800 mb-2">主要症状</h3>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="symptom in selectedDisease.symptoms" 
              :key="symptom"
              class="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-sm"
            >
              {{ symptom }}
            </span>
          </div>
        </div>
        <div v-if="selectedDisease.transmission">
          <h3 class="font-medium text-gray-800 mb-2">传播途径</h3>
          <p class="text-gray-600">{{ selectedDisease.transmission }}</p>
        </div>
        <div v-if="selectedDisease.treatment">
          <h3 class="font-medium text-gray-800 mb-2">治疗方法</h3>
          <p class="text-gray-600">{{ selectedDisease.treatment }}</p>
        </div>
        <div v-if="selectedDisease.prevention">
          <h3 class="font-medium text-gray-800 mb-2">预防措施</h3>
          <p class="text-gray-600">{{ selectedDisease.prevention }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DiseaseCard from '../components/DiseaseCard.vue'
import { diagnosisApi } from '../api/diagnosis'

const diseases = ref([])
const dialogVisible = ref(false)
const selectedDisease = ref(null)

const loadDiseases = async () => {
  try {
    const response = await diagnosisApi.getAllDiseases()
    diseases.value = response.data.data
  } catch (error) {
    console.error('获取疾病列表失败:', error)
  }
}

const showDiseaseDetail = async (diseaseName) => {
  try {
    const response = await diagnosisApi.getDiseaseInfo(diseaseName)
    selectedDisease.value = response.data.data
    dialogVisible.value = true
  } catch (error) {
    console.error('获取疾病详情失败:', error)
  }
}

onMounted(() => {
  loadDiseases()
})
</script>