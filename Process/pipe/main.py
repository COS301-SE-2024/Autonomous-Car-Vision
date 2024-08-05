import os
import cv2
import numpy as np
import imageio
from units import InputUnit, OutputUnit
from depthUnit import DepthEstimationUnit
from pipe import Pipe
from segUnit import SegUnit

def process_video(video_path, output_path, pipe):
    reader = imageio.get_reader(video_path, 'ffmpeg')
    fps = reader.get_meta_data()['fps']
    width, height = reader.get_meta_data()['size']

    writer = imageio.get_writer(output_path, fps=fps)

    try:
        for frame in reader:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
            processed_frame = pipe.process(frame)
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)  # Convert back to RGB for imageio
            writer.append_data(processed_frame)
    finally:
        reader.close()
        writer.close()
        print("Released video reader and writer resources.")

if __name__ == "__main__":
    video_path = "TestEdit.mp4"
    output_path = "output.mp4"

    input_unit = InputUnit()
    seg_unit = SegUnit(model_path='yolov8x-seg.pt')
    output_unit = OutputUnit()

    pipe = Pipe()
    pipe.add_unit(input_unit)
    pipe.add_unit(seg_unit)
    pipe.add_unit(output_unit)

    process_video(video_path, output_path, pipe)