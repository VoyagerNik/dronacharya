import cv2
import numpy as np
import onnxruntime
import os
import time
import logging
  # Import the OCR function

HOME="./" # /home/user/dproj
# Load the ONNX model
onnx_model_path = HOME+"/best.onnx"
session = onnxruntime.InferenceSession(onnx_model_path)

# Input and output folders
input_folder = HOME+"/ip2"  # Folder where images are saved by GStreamer
output_folder = HOME+"/op"
os.makedirs(output_folder, exist_ok=True)

# Set up logging
logging.basicConfig(filename=f'{HOME}/processing.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to process a single image
def process_image(image_path):
    logging.info(f"Processing image: {image_path}")
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            logging.error(f"Error: Unable to read image at {image_path}")
            return

        h, w, _ = image.shape  # Image dimensions

        # Resize image to 640x640 (YOLOv5 expected input size)
        input_size = 640
        image_resized = cv2.resize(image, (input_size, input_size))

        # Preprocess image (YOLOv5 expects 640x640)
        blob = cv2.dnn.blobFromImage(image_resized, 1/255.0, (input_size, input_size), swapRB=True, crop=False)

        # Run inference
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: blob})

        # Extract predictions
        predictions = np.array(outputs[0])

        if predictions.ndim == 3:  
            predictions = predictions[0]  # Remove batch dimension if needed

        conf_threshold = 0.5  # Confidence threshold

        # Find the highest-confidence prediction
        best_prediction = None
        best_confidence = 0

        for pred in predictions:
            if len(pred) < 6:
                continue  # Skip invalid detections

            x_center, y_center, width, height, conf, class_id = pred[:6]

            if conf > conf_threshold and conf > best_confidence:
                best_confidence = conf
                best_prediction = (x_center, y_center, width, height)

        # Crop and save only the best detection
        if best_prediction:
            x_center, y_center, width, height = map(int, best_prediction)

            # Ensure cropping coordinates are within image bounds
            x_min = max(0, x_center - width // 2)
            y_min = max(0, y_center - height // 2)
            x_max = min(w, x_center + width // 2)
            y_max = min(h, y_center + height // 2)

            # Check if the cropping region is valid
            if x_max > x_min and y_max > y_min:
                cropped_img = image_resized[y_min:y_max, x_min:x_max]

                # Save the cropped image
                crop_filename = os.path.join(output_folder, "cropped.jpg")
                cv2.imwrite(crop_filename, cropped_img)
                logging.info(f"Saved cropped image: {crop_filename}")

                # Run OCR on the cropped image
                from pdocr import ocrr
                ocrr()  # Call the OCR function
            else:
                logging.warning("Invalid cropping region. Skipping this image.")
        else:
            logging.warning("No valid container ID detected.")
    except Exception as e:
        logging.error(f"Error processing image {image_path}: {e}")

# Main loop to monitor the input folder
def main_loop():
    processed_images = set()  # Track processed images to avoid reprocessing

    # Wait for the GStreamer pipeline to initialize
    logging.info("Waiting for GStreamer pipeline to initialize...")
    time.sleep(5)  # Adjust the delay as needed
    while True:
        # List all files in the input folder
        image_files = [f for f in os.listdir(input_folder) if f.endswith(".jpg")]
        image_files=sorted(image_files)

        for image_file in image_files:
            if image_file not in processed_images:
                image_path = os.path.join(input_folder, image_file)
                logging.info(f"Processing image: {image_path}")

                # Wait for the image to be fully written (optional)
                time.sleep(1)  # Adjust the delay as needed

                # Process the image
                process_image(image_path)

                # Mark the image as processed
                processed_images.add(image_file)

                # Wait for the output to be written before processing the next image
                time.sleep(2)  # Adjust the delay as needed        i+=1
        # Sleep for a short time before checking for new images again
        time.sleep(1)

if __name__ == "__main__":
    main_loop()
