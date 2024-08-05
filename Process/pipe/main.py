import cv2
import numpy as np
from units import InputUnit, OutputUnit
from depthUnit import DepthEstimationUnit
from segUnit import SegmentationUnit
from pipe import Pipe

def process_video(video_path, pipe):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the original frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize VideoWriter to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height), isColor=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process the current frame through the pipeline
        processed_frame = pipe.process(frame)

        # Write the processed frame to the output video
        if len(processed_frame.shape) == 2:  # If the processed frame is grayscale
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
        out.write(processed_frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    video_path = "C:/Users/keith/Desktop/Autonomous-Car-Vision/Models/petal.mp4"

    # Create units
    input_unit = InputUnit()
    depth_unit = SegmentationUnit()
    output_unit = OutputUnit()

    # Create and configure pipeline
    pipe = Pipe()
    pipe.add_unit(input_unit)
    pipe.add_unit(depth_unit)
    pipe.add_unit(output_unit)

    # Process video
    process_video(video_path, pipe)
