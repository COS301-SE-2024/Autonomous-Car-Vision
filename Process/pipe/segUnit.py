import torch
import cv2
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
from ultralytics import YOLO
from units import Unit
import os


class SegUnit(Unit):
    def __init__(self, model_name, use_tensorrt=False):

        super().__init__(id="SegUnit", input_type=np.ndarray, output_type=np.ndarray)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        if model_name:
            self.model_name = model_name
            self.model_path = f'{model_name}.pt'
            self.model = YOLO(self.model_path).to(self.device)
        else:
            raise ValueError("Model name must be provided")

        # self.frame_width = frame_width
        # self.frame_height = frame_height
        self.use_tensorrt = use_tensorrt

        self.trt_engine = None
        self.context = None

    def process(self, frame):
        if self.use_tensorrt:
            if self.context is None:
                raise RuntimeError("TensorRT engine is not initialized. Call to_tensorrt() first.")
            return self.trt_process(frame)
        else:
            return self.pytorch_process(frame)

    def pytorch_process(self, frame):
        # Ensure the frame is resized to (640, 640) and normalized
        frame = cv2.resize(frame, (640, 640))
        frame = frame / 255.0  # Normalize to [0, 1]
        frame = frame.transpose((2, 0, 1))  # Change from HWC to CHW
        frame = np.expand_dims(frame, axis=0)  # Add batch dimension
        frame = torch.from_numpy(frame).to(self.device).float()

        results = self.model(frame)
        annotated_frame = results[0].plot() if hasattr(results[0], 'masks') else results[0].plot()

        if self.next_unit:
            return self.next_unit.process(annotated_frame)
        return annotated_frame

    def to_tensorrt(self):
        """Convert the model to TensorRT format and update the process method"""
        onnx_model_path = self.model_path.replace('.pt', '.onnx')  # Use the same base name for the ONNX file

        # Correct export command for Ultralytics YOLO model
        self.model.export(format='onnx')  # Specify the output path for the ONNX model

        # Verify ONNX export
        if not os.path.exists(onnx_model_path):
            raise FileNotFoundError(f"ONNX model file '{onnx_model_path}' not found.")

        # Load the ONNX model and create a TensorRT engine
        logger = trt.Logger(trt.Logger.WARNING)
        builder = trt.Builder(logger)
        network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
        parser = trt.OnnxParser(network, logger)

        with open(onnx_model_path, 'rb') as model:
            if not parser.parse(model.read()):
                for error in range(parser.num_errors()):
                    print(parser.get_error(error))
                raise ValueError("Failed to parse the ONNX model")

        config = builder.create_builder_config()
        config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 32)  # 1 GB
        config.set_flag(trt.BuilderFlag.FP16)
        # Code for storing engine:
        # with open(“sample.engine”, “wb”) as f:
        #     f.write(serialized_engine)

        # Allow dynamic shapes
        """
        4.2. Deserializing a Plan
        To perform inference, deserialize the engine using the Runtime interface. Like the builder, the runtime requires an instance of the logger.
        runtime = trt.Runtime(logger)
        You can then deserialize the engine from a memory buffer:
        engine = runtime.deserialize_cuda_engine(serialized_engine)
        If you want, first load the engine from a file:
        with open(“sample.engine”, “rb”) as f:
            serialized_engine = f.read()
        """
        profile = builder.create_optimization_profile()
        profile.set_shape(network.get_input(0).name, (1, 3, 640, 640), (1, 3, 640, 640), (1, 3, 640, 640))
        config.add_optimization_profile(profile)

        # Build the engine
        serialized_engine = builder.build_serialized_network(network, config)
        if serialized_engine is None:
            raise RuntimeError("Failed to build the TensorRT engine")
        runtime = trt.Runtime(logger)
        self.trt_engine = runtime.deserialize_cuda_engine(serialized_engine)
        self.context = self.trt_engine.create_execution_context()

        print(f"Model {self.model_path} converted to TensorRT")

    def trt_process(self, frame):
        frame = cv2.resize(frame, (640, 640))
        frame = frame / 255.0  # Normalize to [0, 1]
        frame = frame.transpose((2, 0, 1))  # Change from HWC to CHW
        frame = np.expand_dims(frame, axis=0).astype(np.float32)  # Add batch dimension and convert to float32

        input_shape = frame.shape
        output_shape = (1, -1, 640, 640)  # Example output shape
        d_input = cuda.mem_alloc(trt.get_element_count(input_shape) * np.dtype(np.float32).itemsize)
        d_output = cuda.mem_alloc(trt.get_element_count(output_shape) * np.dtype(np.float32).itemsize)
        stream = cuda.Stream()

        # Bind the input and output buffers
        bindings = [int(d_input), int(d_output)]

        # Copy the input data to the device
        cuda.memcpy_htod_async(d_input, frame, stream)

        # Execute the TensorRT engine
        self.context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)

        # Allocate output memory and copy the output data from the device
        output_data = np.empty(output_shape, dtype=np.float32)
        cuda.memcpy_dtoh_async(output_data, d_output, stream)
        stream.synchronize()

        output_data = np.clip(output_data, 0, 255).astype(np.uint8)

        if self.next_unit:
            return self.next_unit.process(output_data)
        return output_data