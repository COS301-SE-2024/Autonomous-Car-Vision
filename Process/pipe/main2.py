import os
import cv2
import numpy as np
import imageio
from units import InputUnit, OutputUnit
import yoloUnit4
from pipe import Pipe

def preprocess_frame(frame, target_size=(640, 640)):
    """Resize frame to the target size while maintaining aspect ratio with padding."""
    height, width = frame.shape[:2]
    scale = min(target_size[0] / height, target_size[1] / width)
    resized = cv2.resize(frame, (int(width * scale), int(height * scale)))
    pad_height = (target_size[0] - resized.shape[0]) // 2
    pad_width = (target_size[1] - resized.shape[1]) // 2
    padded = cv2.copyMakeBorder(resized, pad_height, pad_height, pad_width, pad_width, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    return padded

def postprocess_frame(frame, original_size=(1920, 1080)):
    """Resize frame back to the original size."""
    return cv2.resize(frame, original_size)

def process_video(video_path, output_path, pipe):
    reader = imageio.get_reader(video_path, 'ffmpeg')
    fps = reader.get_meta_data()['fps']
    width, height = reader.get_meta_data()['size']

    writer = imageio.get_writer(output_path, fps=fps)

    try:
        for frame in reader:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
            preprocessed_frame = preprocess_frame(frame)
            processed_frame = pipe.process(preprocessed_frame)
            postprocessed_frame = postprocess_frame(processed_frame, (width, height))
            postprocessed_frame = cv2.cvtColor(postprocessed_frame, cv2.COLOR_BGR2RGB)  # Convert back to RGB for imageio
            writer.append_data(postprocessed_frame)
    finally:
        reader.close()
        writer.close()
        print("Released video reader and writer resources.")

if __name__ == "__main__":
    video_path = "petal.mp4"
    output_path = "output.mp4"

    input_unit = InputUnit()
    seg_unit = yoloUnit4.SegUnit('yolov8n-seg', 640, 640, use_tensorrt=True)
    output_unit = OutputUnit()

    pipe = Pipe()
    pipe.add_unit(input_unit)
    pipe.add_unit(seg_unit)
    pipe.add_unit(output_unit)

    # Convert all units to TensorRT
    for unit in [seg_unit]:
        unit.to_tensorrt()

    process_video(video_path, output_path, pipe)
