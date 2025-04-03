import cv2
import numpy as np
import onnxruntime as ort
from paddleocr import PaddleOCR
HOME="/app" # /home/user/dproj

# Paths
def ocrr():
    det_model_path = "/app/det_model.onnx"
    rec_model_path = "/app/rec_model.onnx"
    image_path = "/app/op/cropped.jpg"  # Change this to your image path

    # Load PaddleOCR with custom ONNX models
    ocr = PaddleOCR(det_model_path=det_model_path, rec_model_path=rec_model_path, use_angle_cls=True, use_gpu=False)

    # Run OCR
    results = ocr.ocr(image_path, cls=True)

    # Extract First 10 Characters
    full_text = ""
    for result in results:
        for line in result:
            full_text += line[1][0]  # Append detected text

    first_10_chars = full_text[:10]  # Take only first 10 characters
    rearranged=first_10_chars
    #rearranged= first_10_chars[-4:] + first_10_chars[:-4]
    with open("/app/outuput.txt", "a") as file:
        file.write(rearranged + "\n") 

    # Print and Save
    print(rearranged)

ocrr()