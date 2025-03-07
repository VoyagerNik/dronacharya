import cv2
import numpy as np
import onnxruntime
import os

# Load the ONNX model
onnx_model_path = "C:\\Users\\Aniruth\\Downloads\\best.onnx"
session = onnxruntime.InferenceSession(onnx_model_path)

# Input image
image_path = "C:\\Users\\Aniruth\\Desktop\\yolov5\\datasets\\roboflow\\train\\images\\1_JPG_jpg.rf.7ca0f634bf00f665024902b7c5639412.jpg"

# Output folder
output_folder = "C:\\Users\\Aniruth\\Desktop\\cropped_img"
os.makedirs(output_folder, exist_ok=True)

# Read image
image = cv2.imread(image_path)
if image is None:
    print(f"Error: Unable to read image at {image_path}")
    exit()

h, w, _ = image.shape  # Image dimensions

# Preprocess image (YOLOv5 expects 640x640)
input_size = 640
blob = cv2.dnn.blobFromImage(image, 1/255.0, (input_size, input_size), swapRB=True, crop=False)

# Run inference
input_name = session.get_inputs()[0].name
outputs = session.run(None, {input_name: blob})

# Extract predictions
predictions = np.array(outputs[0])

if predictions.ndim == 3:  
    predictions = predictions[0]  # Remove batch dimension if needed

conf_threshold = 0.5  # Confidence threshold

# **Find the highest-confidence prediction**
best_prediction = None
best_confidence = 0

for pred in predictions:
    if len(pred) < 6:
        continue  # Skip invalid detections

    x_center, y_center, width, height, conf, class_id = pred[:6]

    if conf > conf_threshold and conf > best_confidence:
        best_confidence = conf
        best_prediction = (x_center, y_center, width, height)

# **Crop and save only the best detection**
if best_prediction:
    x_center, y_center, width, height = map(int, best_prediction)

    x_min = max(0, x_center - width // 2)
    y_min = max(0, y_center - height // 2)
    x_max = min(w, x_center + width // 2)
    y_max = min(h, y_center + height // 2)

    cropped_img = image[y_min:y_max, x_min:x_max]

    crop_filename = os.path.join(output_folder, "cropped.jpg")
    cv2.imwrite(crop_filename, cropped_img)
    print(f"Saved cropped image: {crop_filename}")
else:
    print("No valid container ID detected.")

