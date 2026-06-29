from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "猪病诊断智能体"
    app_version: str = "1.0.0"
    database_url: str = "sqlite+aiosqlite:///./pig_disease.db"
    upload_dir: str = "./uploads"
    model_dir: str = "./models"
    confidence_threshold: float = 0.7
    max_image_size: int = 5 * 1024 * 1024
    api_prefix: str = "/api"
    allowed_origins: list = ["*"]
    disease_list: list = [
        '非洲猪瘟', '猪瘟', '猪口蹄疫', '猪繁殖与呼吸综合征',
        '猪圆环病毒病', '猪传染性胃肠炎', '猪伪狂犬病', '猪链球菌病',
        '副猪嗜血杆菌病', '猪丹毒', '猪传染性胸膜肺炎', '猪附红细胞体病'
    ]

    class Config:
        env_file = ".env"

settings = Settings()