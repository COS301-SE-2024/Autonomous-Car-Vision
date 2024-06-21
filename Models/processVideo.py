import cv2
import os
from ultralytics import YOLO

def process_video(input_video_path, output_video_path, model_path='yolov8n/yolov8n.pt'):
    # Load the YOLOv8 model
    model = YOLO(model_path)  # Ensure the path to your YOLOv8 model is correct

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
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Write the annotated frame to the output video
            out.write(annotated_frame)

            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture and writer objects and close the display window
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Example usage
    process_video("testVid.mp4", "outputs/annotated_testVid.mp4")