import torch
from torchvision import transforms
from PIL import Image
import timm

class FoodClassifier:

    def __init__(self):
        self.model = timm.create_model(
            "resnet50",
            pretrained=True
        )
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

        # Simplified label list (replace with Food-101 labels later)
        self.labels = [
            "pizza", "fried_rice", "ramen", "burger",
            "salad", "steak", "omelette", "pasta"
        ]

    def predict(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image = self.transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(image)

        predicted = torch.argmax(outputs, dim=1).item()

        return self.labels[predicted % len(self.labels)]