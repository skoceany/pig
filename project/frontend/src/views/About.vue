<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h2 class="text-xl font-bold text-gray-800 mb-6">关于猪病诊断智能体</h2>
    
    <div class="space-y-6">
      <div>
        <h3 class="font-medium text-gray-800 mb-2">项目介绍</h3>
        <p class="text-gray-600">
          猪病诊断智能体是基于大模型技术构建的智能养殖辅助系统，能够通过分析猪的照片，
          自动识别猪是否患病以及具体患的是什么病，并提供详细的疾病解读和应对建议。
        </p>
      </div>
      
      <div>
        <h3 class="font-medium text-gray-800 mb-2">技术架构</h3>
        <ul class="text-gray-600 space-y-2">
          <li>• 前端：Vue.js 3 + Element Plus + Tailwind CSS</li>
          <li>• 后端：FastAPI + Python</li>
          <li>• AI模型：多模态大模型（LLaVA/Qwen-VL）</li>
          <li>• 数据库：SQLite</li>
        </ul>
      </div>
      
      <div>
        <h3 class="font-medium text-gray-800 mb-2">支持的疾病类型</h3>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
          <span v-for="disease in diseaseList" :key="disease" class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm">
            {{ disease }}
          </span>
        </div>
      </div>
      
      <div>
        <h3 class="font-medium text-gray-800 mb-2">使用方法</h3>
        <ol class="text-gray-600 space-y-2 list-decimal list-inside">
          <li>点击首页的上传按钮，选择猪的照片</li>
          <li>等待AI分析，通常需要几秒钟</li>
          <li>查看诊断结果和疾病解读</li>
          <li>如需了解更多疾病信息，可访问疾病知识库</li>
        </ol>
      </div>
      
      <div>
        <h3 class="font-medium text-gray-800 mb-2">注意事项</h3>
        <ul class="text-gray-600 space-y-2 list-disc list-inside">
          <li>本系统仅供参考，不能替代专业兽医的诊断</li>
          <li>如发现猪有异常，建议及时联系专业兽医</li>
          <li>上传的图片应清晰，以便获得更准确的诊断结果</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
const diseaseList = [
  '非洲猪瘟', '猪瘟', '猪口蹄疫', '猪繁殖与呼吸综合征',
  '猪圆环病毒病', '猪传染性胃肠炎', '猪伪狂犬病', '猪链球菌病',
  '副猪嗜血杆菌病', '猪丹毒', '猪传染性胸膜肺炎', '猪附红细胞体病'
]
</script>