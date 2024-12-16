#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import argparse
from ultralytics import YOLO
import cv2
from matplotlib import pyplot as plt
import os
import pandas as pd

def main(model_path, image_folder, results_folder):
    # Define the paths
    excel_output_path = os.path.join(results_folder, "detection_results.xlsx")

    # Create the results folder if it doesn't exist
    os.makedirs(results_folder, exist_ok=True)

    # Load the model
    model = YOLO(model_path)

    # Initialize a list to store detection data
    detection_data = []

    # Loop through all images in the folder
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_path = os.path.join(image_folder, filename)
            
            # Load the image
            original_image = cv2.imread(image_path)
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for correct colors
            
            # Perform inference
            results = model(image_path)
            
            # Draw the bounding boxes on the original image
            for result in results:
                for i, box in enumerate(result.boxes.xyxy):  # Bounding box coordinates (xmin, ymin, xmax, ymax)
                    x1, y1, x2, y2 = map(int, box[:4])  # Convert to integers
                    label = result.names[int(result.boxes.cls[i].item())]  # Class label
                    confidence = result.boxes.conf[i].item()  # Confidence score
                    
                    # Draw the bounding box
                    cv2.rectangle(original_image, (x1, y1), (x2, y2), color=(255, 0, 0), thickness=2)  # Blue box
                    
                    # Draw the label
                    text = f"{label} {confidence:.2f}"
                    cv2.putText(original_image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    
                    # Append detection data
                    detection_data.append({"Filename": filename, "Label": label, "Confidence": confidence})
            
            # Save the resulting image
            output_path = os.path.join(results_folder, filename)  # Save with the same file name
            cv2.imwrite(output_path, cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR))  # Convert back to BGR for saving

            print(f"Processed image saved to: {output_path}")

    # Create a DataFrame and save to Excel
    df = pd.DataFrame(detection_data)
    df.to_excel(excel_output_path, index=False)

    print(f"Detection results saved to: {excel_output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run YOLO detection on a folder of images.")
    parser.add_argument("model_path", type=str, help="Path to the YOLO model file (e.g., best.pt)")
    parser.add_argument("image_folder", type=str, help="Path to the folder containing images for detection")
    parser.add_argument("results_folder", type=str, help="Path to the folder where results will be saved")
    
    args = parser.parse_args()
    main(args.model_path, args.image_folder, args.results_folder)

