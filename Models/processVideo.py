import sys
import cv2
import os
from ultralytics import YOLO

def process_video(input_video_path, output_video_path, model_path='yolov8n/yolov8n.pt'):
    model = YOLO(model_path)

    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_video_path)
    os.makedirs(output_dir, exist_ok=True)

    # Input from video
    cap = cv2.VideoCapture(input_video_path)

    # Get the video frame width, height, and frames per second (fps)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
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

            # Write the annotated frame to the output video
            out.write(annotated_frame)
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture and writer objects
    cap.release()
    out.release()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)
    input_video_path = sys.argv[1]
    output_video_path = sys.argv[2]
    model_path = sys.argv[3]
    process_video(input_video_path, output_video_path, model_path)