from PIL import Image
import torch
from torchvision import transforms

def preprocess_image(image_path, target_size=(224, 224)):
    image = Image.open(image_path).convert('RGB')
    return image

async def save_image(image_file, save_path):
    content = await image_file.read()
    with open(save_path, 'wb') as f:
        f.write(content)

def augment_image(image):
    transforms_list = [
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0)),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1))
    ]
    augmented_images = []
    for transform in transforms_list:
        augmented_images.append(transform(image))
    return augmented_images