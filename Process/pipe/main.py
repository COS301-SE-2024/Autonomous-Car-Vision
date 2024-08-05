import cv2
import numpy as np
from units import InputUnit, OutputUnit
from depthUnit import DepthEstimationUnit
from pipe import Pipe
from segUnit import SegUnit

def process_video(video_path, pipe):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = pipe.process(frame)
        out.write(processed_frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    video_path = "TestEdit.mp4"

    input_unit = InputUnit()
    seg_unit = SegUnit(model_path='yolov8x-seg.pt')
    output_unit = OutputUnit()

    pipe = Pipe()
    pipe.add_unit(input_unit)
    pipe.add_unit(seg_unit)
    pipe.add_unit(output_unit)

    process_video(video_path, pipe)