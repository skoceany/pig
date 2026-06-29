import os
import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoProcessor, AutoModelForVisionAndLanguageGeneration, AdamW
from tqdm import tqdm

class PigDiseaseDataset(Dataset):
    def __init__(self, data_dir, processor):
        self.data_dir = data_dir
        self.processor = processor
        self.samples = self._load_samples()

    def _load_samples(self):
        samples = []
        disease_dirs = [d for d in os.listdir(self.data_dir) if os.path.isdir(os.path.join(self.data_dir, d))]
        for disease_name in disease_dirs:
            disease_path = os.path.join(self.data_dir, disease_name)
            description_path = os.path.join(disease_path, "描述.txt")
            if os.path.exists(description_path):
                with open(description_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                description = self._extract_description(content, disease_name)
                images = [f for f in os.listdir(disease_path) if f.endswith('.jpg')]
                for image_file in images[:5]:
                    image_path = os.path.join(disease_path, image_file)
                    samples.append({
                        'image_path': image_path,
                        'disease_name': disease_name,
                        'description': description
                    })
        return samples

    def _extract_description(self, content, disease_name):
        lines = content.strip().split('\n')
        description = []
        for line in lines:
            if line and not line.endswith('.jpg') and line != disease_name:
                description.append(line)
        return '\n'.join(description)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        image = self.processor(images=sample['image_path'], return_tensors="pt").pixel_values[0]
        text = f"疾病名称: {sample['disease_name']}\n疾病描述: {sample['description']}"
        encoding = self.processor(text=text, return_tensors="pt", padding="max_length", truncation=True)
        labels = encoding.input_ids.clone()
        return {
            'pixel_values': image,
            'input_ids': encoding.input_ids[0],
            'attention_mask': encoding.attention_mask[0],
            'labels': labels[0]
        }

def train_model():
    processor = AutoProcessor.from_pretrained("LLaVA-7B")
    model = AutoModelForVisionAndLanguageGeneration.from_pretrained("LLaVA-7B")
    model.train()

    dataset = PigDiseaseDataset("../../多模态数据/train-data", processor)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    optimizer = AdamW(model.parameters(), lr=5e-5)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    num_epochs = 3
    for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")
        total_loss = 0
        for batch in tqdm(dataloader):
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            total_loss += loss.item()
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        print(f"Loss: {total_loss / len(dataloader)}")

    model.save_pretrained("../../backend/models/pig_disease_model")
    processor.save_pretrained("../../backend/models/pig_disease_model")
    print("模型训练完成并保存")

if __name__ == "__main__":
    train_model()