import os
import json

def load_disease_descriptions(data_dir="./多模态数据/train-data"):
    diseases = []
    disease_dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    for disease_name in disease_dirs:
        description_path = os.path.join(data_dir, disease_name, "描述.txt")
        if os.path.exists(description_path):
            with open(description_path, 'r', encoding='utf-8') as f:
                content = f.read()
            disease_info = parse_description_file(disease_name, content)
            diseases.append(disease_info)
    return diseases

def parse_description_file(disease_name, content):
    lines = content.strip().split('\n')
    description = []
    symptoms = []
    image_descriptions = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line == disease_name:
            i += 1
            continue
        if line.endswith('.jpg'):
            if i + 1 < len(lines) and not lines[i+1].strip().endswith('.jpg'):
                image_descriptions.append(lines[i+1].strip())
                symptoms.extend(extract_symptoms(lines[i+1].strip()))
            i += 2
            continue
        description.append(line)
        i += 1
    return {
        'disease_name': disease_name,
        'description': '\n'.join(description),
        'symptoms': json.dumps(list(set(symptoms))),
        'transmission': '',
        'treatment': '',
        'prevention': '',
        'images_count': len(image_descriptions)
    }

def extract_symptoms(text):
    symptom_keywords = [
        '出血', '发绀', '水泡', '肿胀', '红斑', '疹块', '溃疡',
        '发烧', '高烧', '腹泻', '呕吐', '瘫痪', '坏死', '充血',
        '水肿', '呼吸困难', '精神沉郁', '食欲不振'
    ]
    symptoms = []
    for keyword in symptom_keywords:
        if keyword in text:
            symptoms.append(keyword)
    return symptoms