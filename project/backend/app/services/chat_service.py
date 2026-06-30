import json
import asyncio
from app.config.settings import settings
from app.models.pig_disease_model import DISEASE_KNOWLEDGE

class ChatService:
    def __init__(self):
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self):
        diseases_info = "\n".join([
            f"- {name}: {info['description'][:50]}..." 
            for name, info in DISEASE_KNOWLEDGE.items()
        ])
        
        return f"""你是一个专业的猪病诊断智能助手，擅长回答关于猪病的各种问题。

可用疾病知识库（12种猪病）：
{diseases_info}

回答准则：
1. 对于疾病诊断相关的问题，优先使用知识库中的信息
2. 如果用户询问疾病的症状或防治措施，请提供详细、专业的回答
3. 如果用户上传了图片并得到诊断结果，可以结合诊断结果进行分析
4. 保持回答简洁明了，避免使用过于专业的术语让用户难以理解
5. 如果问题超出猪病范围，请礼貌告知用户你是猪病诊断专家

请以专业兽医助手的身份回答问题。"""

    async def chat(self, message):
        return await self._get_response(message)

    async def chat_with_history(self, messages):
        full_messages = [{"role": "system", "content": self.system_prompt}]
        full_messages.extend(messages)
        return await self._get_response_with_history(full_messages)

    async def _get_response(self, message):
        try:
            if settings.llm_api_key:
                return await self._call_llm(message)
            else:
                return self._get_mock_response(message)
        except Exception:
            return self._get_mock_response(message)

    async def _get_response_with_history(self, messages):
        try:
            if settings.llm_api_key:
                return await self._call_llm_with_history(messages)
            else:
                return self._get_mock_response(messages[-1]["content"])
        except Exception:
            return self._get_mock_response(messages[-1]["content"])

    async def _call_llm(self, message):
        import httpx
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.llm_api_key}"
        }
        
        data = {
            "model": settings.llm_model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.llm_api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

    async def _call_llm_with_history(self, messages):
        import httpx
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.llm_api_key}"
        }
        
        data = {
            "model": settings.llm_model,
            "messages": messages,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.llm_api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

    def _get_mock_response(self, message):
        message_lower = message.lower()
        
        for disease_name, info in DISEASE_KNOWLEDGE.items():
            if disease_name in message or disease_name.lower() in message_lower:
                return f"{disease_name}：\n\n描述：{info['description']}\n\n主要症状：{', '.join(info['symptoms'])}\n\n建议措施：{', '.join(info['recommendations'])}"
        
        if any(keyword in message_lower for keyword in ['发烧', '发热', '高烧']):
            return "猪出现发热症状可能由多种疾病引起，常见原因包括：\n\n1. 猪瘟：高热稽留，伴有皮肤出血点\n2. 非洲猪瘟：急性高热，死亡率极高\n3. 猪链球菌病：高热，可能伴有关节炎\n4. 猪丹毒：急性型高热皮肤发红\n\n建议：\n- 立即测量体温，观察其他症状\n- 隔离病猪，避免传染\n- 及时咨询兽医进行专业诊断"
        
        if any(keyword in message_lower for keyword in ['咳嗽', '呼吸', '气喘']):
            return "猪出现呼吸道症状可能由以下疾病引起：\n\n1. 猪传染性胸膜肺炎：高热、呼吸困难、口鼻流出血色泡沫\n2. 猪繁殖与呼吸综合征（蓝耳病）：呼吸困难、发热\n3. 副猪嗜血杆菌病：咳嗽、呼吸困难、关节肿胀\n\n建议：\n- 加强通风，保持圈舍空气流通\n- 降低饲养密度\n- 及时使用敏感抗生素治疗"
        
        if any(keyword in message_lower for keyword in ['腹泻', '拉稀', '拉肚子']):
            return "猪腹泻可能由以下原因引起：\n\n1. 猪传染性胃肠炎：呕吐、水样腹泻\n2. 猪圆环病毒病：腹泻、消瘦\n3. 猪瘟：腹泻或便秘交替\n\n建议：\n- 补充电解质，防止脱水\n- 使用抗生素预防继发感染\n- 保持圈舍清洁干燥"
        
        if any(keyword in message_lower for keyword in ['疫苗', '免疫']):
            return "猪病疫苗接种建议：\n\n1. 猪瘟疫苗：仔猪21日龄首免，60日龄二免\n2. 口蹄疫疫苗：每年春秋各接种一次\n3. 猪伪狂犬病疫苗：母猪产前接种，仔猪断奶后接种\n4. 猪圆环病毒病疫苗：仔猪2-4周龄接种\n5. 猪繁殖与呼吸综合征疫苗：根据当地疫情情况接种\n\n建议制定科学的免疫程序，定期接种。"
        
        return "您好！我是猪病诊断智能助手。\n\n我可以帮助您：\n- 识别猪的疾病症状\n- 提供疾病防治建议\n- 解答养殖相关问题\n\n您可以上传猪的照片进行疾病诊断，或者直接询问关于猪病的问题。\n\n系统支持识别以下12种猪病：非洲猪瘟、猪瘟、猪口蹄疫、猪繁殖与呼吸综合征、猪圆环病毒病、猪传染性胃肠炎、猪伪狂犬病、猪链球菌病、副猪嗜血杆菌病、猪丹毒、猪传染性胸膜肺炎、猪附红细胞体病。"