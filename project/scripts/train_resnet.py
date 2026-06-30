import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
from tqdm import tqdm
import json

DATA_DIR = "../../../2026-6-28多模态数据/train-data"
MODEL_SAVE_PATH = "../backend/models/pig_disease_model.pth"
LABELS_JSON_PATH = "../backend/models/disease_labels.json"

DISEASE_LIST = [
    '非洲猪瘟', '猪瘟', '猪口蹄疫', '猪繁殖与呼吸综合征',
    '猪圆环病毒病', '猪传染性胃肠炎', '猪伪狂犬病', '猪链球菌病',
    '副猪嗜血杆菌病', '猪丹毒', '猪传染性胸膜肺炎', '猪附红细胞体病'
]

class PigDiseaseDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.samples = []
        self._load_samples()

    def _load_samples(self):
        for idx, disease_name in enumerate(DISEASE_LIST):
            disease_path = os.path.join(self.data_dir, disease_name)
            if os.path.isdir(disease_path):
                images = [f for f in os.listdir(disease_path) if f.endswith('.jpg')]
                for image_file in images:
                    image_path = os.path.join(disease_path, image_file)
                    self.samples.append((image_path, idx))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        image_path, label = self.samples[idx]
        image = Image.open(image_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, label

def train_model():
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    full_dataset = PigDiseaseDataset(DATA_DIR, transform=train_transform)
    dataset_size = len(full_dataset)
    train_size = int(0.8 * dataset_size)
    val_size = dataset_size - train_size

    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])
    val_dataset.dataset.transform = val_transform

    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=0)

    model = models.resnet50(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(DISEASE_LIST))

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

    num_epochs = 15
    best_acc = 0.0

    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch + 1}/{num_epochs}")
        print('-' * 30)

        model.train()
        train_loss = 0.0
        train_correct = 0

        for images, labels in tqdm(train_loader):
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            train_correct += torch.sum(preds == labels.data)

        train_loss = train_loss / len(train_loader.dataset)
        train_acc = train_correct.double() / len(train_loader.dataset)

        print(f"训练集 - Loss: {train_loss:.4f}, Acc: {train_acc:.4f}")

        model.eval()
        val_loss = 0.0
        val_correct = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data)

        val_loss = val_loss / len(val_loader.dataset)
        val_acc = val_correct.double() / len(val_loader.dataset)

        print(f"验证集 - Loss: {val_loss:.4f}, Acc: {val_acc:.4f}")

        scheduler.step()

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"保存最佳模型，准确率: {best_acc:.4f}")

    with open(LABELS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(DISEASE_LIST, f, ensure_ascii=False)

    print(f"\n训练完成！最佳验证准确率: {best_acc:.4f}")
    print(f"模型已保存至: {MODEL_SAVE_PATH}")
    print(f"标签文件已保存至: {LABELS_JSON_PATH}")

if __name__ == "__main__":
    train_model()
