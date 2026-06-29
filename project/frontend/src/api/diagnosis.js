import axios from 'axios'

const API_BASE_URL = '/api'

export const diagnosisApi = {
  async diagnose(formData) {
    return axios.post(`${API_BASE_URL}/diagnosis`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  async getDiseaseInfo(diseaseName) {
    return axios.get(`${API_BASE_URL}/disease/${encodeURIComponent(diseaseName)}`)
  },
  async getAllDiseases() {
    return axios.get(`${API_BASE_URL}/disease/`)
  },
  async getHistory(params) {
    return axios.get(`${API_BASE_URL}/history`, { params })
  },
  async deleteHistory(recordId) {
    return axios.delete(`${API_BASE_URL}/history/${recordId}`)
  }
}