import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import cv2

class VideoEntropyCalibrator(trt.IInt8EntropyCalibrator2):
    def __init__(self, video_path, batch_size=1):
        super().__init__()
        self.batch_size = batch_size
        self.frame_width = 640
        self.frame_height = 640
        self.video_path = video_path
        self.video_capture = cv2.VideoCapture(video_path)
        self.d_input = cuda.mem_alloc(self.batch_size * self.frame_width * self.frame_height * 3 * np.dtype(np.float32).itemsize)
        self.batch = np.zeros((self.batch_size, 3, self.frame_height, self.frame_width), dtype=np.float32)
        self.done = False

    def get_batch_size(self):
        return self.batch_size

    def get_batch(self, names):
        if self.done:
            return None

        frames = []
        for _ in range(self.batch_size):
            ret, frame = self.video_capture.read()
            if not ret:
                self.done = True
                return None

            frame = cv2.resize(frame, (self.frame_width, self.frame_height))
            frame = frame / 255.0  # Normalize to [0, 1]
            frame = frame.transpose((2, 0, 1))  # Change from HWC to CHW
            frames.append(frame)

        self.batch = np.stack(frames).astype(np.float32)
        cuda.memcpy_htod(self.d_input, self.batch)
        return [int(self.d_input)]

    def read_calibration_cache(self):
        return None

    def write_calibration_cache(self, cache):
        return None
