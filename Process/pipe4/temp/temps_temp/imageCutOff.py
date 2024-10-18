import cv2
import numpy as np
from ultralytics import YOLO  # YOLO model from ultralytics

def process_image(image_path, cutoff_percent=20):
    # Load the original image
    image = cv2.imread(image_path)
    
    # Get original image dimensions
    original_height, original_width = image.shape[:2]
    
    # Calculate the height of the cropped image
    crop_height = int(original_height * (1 - cutoff_percent / 100.0))
    
    # Crop the image (keep only the top part)
    cropped_image = image[:crop_height, :]
    
    # Initialize the YOLOv8n model (object detection)
    model = YOLO('laneTest.pt')  # Use the yolov8n model

    # Perform detection on the cropped image
    results = model(cropped_image)

    # Create a mask to store the segmented area for the original image size
    colored_mask = np.zeros_like(image, dtype=np.uint8)
    
    # Process each detection result
    for result in results:
        # If segmentation is present in results
        if hasattr(result, 'masks') and result.masks is not None:
            # Loop through the segmentation masks
            masks = result.masks.data.cpu().numpy()
            for mask in masks:
                mask = np.squeeze(mask)
                
                # Resize the mask to the original image's width and crop_height height
                resized_mask = cv2.resize(mask, (original_width, crop_height), interpolation=cv2.INTER_NEAREST)
                
                # Convert the mask to binary
                binary_mask = (resized_mask > 0.5).astype(np.uint8)
                
                # Convert binary mask to 3 channels to apply on the original image
                binary_mask_3d = np.stack([binary_mask] * 3, axis=-1)
                
                # Apply the mask directly to the corresponding region of the original image
                colored_mask[:crop_height, :] = binary_mask_3d * 255  # White color for mask
                
        # If bounding boxes are present in the results
        if hasattr(result, 'boxes') and result.boxes is not None:
            for box in result.boxes:
                # Extract bounding box coordinates
                x_min, y_min, x_max, y_max = map(int, box.xyxy[0].cpu().numpy())
                
                # Draw the bounding box on the corresponding area of the original image
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    
    # Overlay the segmentation mask on the original image
    alpha = 0.5  # Transparency factor for mask overlay
    output_image = cv2.addWeighted(image, 1 - alpha, colored_mask, alpha, 0)
    
    # Display the output image with segmentation and bounding boxes
    cv2.imshow('Segmented Image', output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = 'image.png'  # Replace with your image path
cutoff_percent = 37  # Adjust the crop percentage

process_image(image_path, cutoff_percent)
