import cv2

# Load the image
image = cv2.imread('UIPageScreenshot.png')

# Define bounding boxes and labels
# Each bounding box is a tuple: (x, y, width, height)
# Each label is a string
bounding_boxes = [(50, 50, 200, 200), (300, 300, 200, 200)]
labels = ['list box', 'button']

# Draw each bounding box and label on the image
for (x, y, w, h), label in zip(bounding_boxes, labels):
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

# Display the image
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()