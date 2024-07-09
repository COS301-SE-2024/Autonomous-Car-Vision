import sys
import os
import torch
import cv2
import imageio
from ultralytics import YOLO

def process_video(input_video_path, output_video_path, model_path='yolov8n.pt'):
    # Check if CUDA is available and set the device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Load the model with the specified device
    model = YOLO(model_path).to(device)

    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_video_path)
    os.makedirs(output_dir, exist_ok=True)

    # Input from video
    reader = imageio.get_reader(input_video_path, 'ffmpeg')
    fps = reader.get_meta_data()['fps']
    width, height = reader.get_meta_data()['size']

    # Create a writer object
    writer = imageio.get_writer(output_video_path, fps=fps)

    for frame in reader:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

        # Run YOLOv8 model on the frame
        results = model(frame)

        # Check if the model is a segmentation model (SAM)
        if hasattr(results[0], 'masks'):
            # Handle segmentation/masking
            annotated_frame = results[0].plot()  # Assuming results[0].plot() plots the masks
            
            # If not, you need to manually plot masks using OpenCV
            # for mask in results[0].masks:
            #     frame[mask] = (0, 255, 0)  # Example: filling mask with green color
        else:
            # Handle normal object detection
            annotated_frame = results[0].plot()

        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)  # Convert back to RGB for imageio
        writer.append_data(annotated_frame)

    # Release the writer object
    writer.close()
    print("Processing complete.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_video_path> <output_video_path> <model_path>")
        sys.exit(1)
    input_video_path = sys.argv[1]
    output_video_path = sys.argv[2]
    model_path = sys.argv[3]
    process_video(input_video_path, output_video_path, model_path)