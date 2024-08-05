import cv2
import numpy as np
from units import InputUnit, OutputUnit
from depthUnit import DepthEstimationUnit
from pipe import Pipe

def process_video(video_path, pipe):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the current frame through the pipeline
        processed_frame = pipe.process(frame)

        # Display the frame and processed result
        cv2.imshow('Frame', frame)
        cv2.imshow('Processed Frame', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "C:/Users/Keith/Downloads/petal_20240623_172724.mp4"

    # Create units
    input_unit = InputUnit()
    depth_estimation_unit = DepthEstimationUnit()
    output_unit = OutputUnit()

    # Create and configure pipeline
    pipe = Pipe()
    pipe.add_unit(input_unit)
    pipe.add_unit(depth_estimation_unit)
    pipe.add_unit(output_unit)

    # Process video
    process_video(video_path, pipe)
