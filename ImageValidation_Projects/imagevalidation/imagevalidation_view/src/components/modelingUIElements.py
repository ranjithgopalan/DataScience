import cv2
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn

# Load the trained model
model = fasterrcnn_resnet50_fpn(pretrained=False)
model.load_state_dict(torch.load('resnet50-0676ba61.pth'))
model.eval()
print(model.share_memory())

# Load the image
image = cv2.imread('combined.png')

# Convert the image to a torch tensor
image = torch.from_numpy(image).float().permute(2, 0, 1)

# Use the model to identify UI elements in the image
output = model([image])

# Print the bounding boxes and labels of the identified UI elements
for box, label in zip(output[0]['boxes'], output[0]['labels']):
    print(f'Found a {label} at {box}')