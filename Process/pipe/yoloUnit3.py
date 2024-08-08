import cv2
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
from ultralytics import YOLO
from units import Unit
import os
import torch

class SegUnit(Unit):
    def __init__(self, model_name, frame_width, frame_height, use_tensorrt=False):
        super().__init__(id="SegUnit", input_type=np.ndarray, output_type=np.ndarray)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")

        if model_name:
            self.model_name = model_name
            self.model_path = f'{model_name}.pt'
            self.model = YOLO(self.model_path).to(self.device)
        else:
            raise ValueError("Model name must be provided")

        self.frame_width = frame_width
        self.frame_height = frame_height
        self.use_tensorrt = use_tensorrt

        self.trt_engine = None
        self.context = None

        # Allocate buffers during initialization
        self.d_input = None
        self.d_output = None

    def process(self, frame):
        if self.use_tensorrt:
            if self.context is None:
                raise RuntimeError("TensorRT engine is not initialized. Call to_tensorrt() first.")
            return self.trt_process(frame)
        else:
            return self.pytorch_process(frame)

    def pytorch_process(self, frame):
        # Normalize the frame
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
        onnx_model_path = self.model_path.replace('.pt', '.onnx')

        # Export the model to ONNX format
        self.model.export(format='onnx')

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
        config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 32)  # Increase workspace to 4 GB
        config.set_flag(trt.BuilderFlag.FP16)  # Enable FP16 precision

        # Set the optimization profile based on the provided frame sizes
        profile = builder.create_optimization_profile()
        profile.set_shape(network.get_input(0).name,
                          (1, 3, self.frame_height, self.frame_width),  # Minimum shape
                          (4, 3, self.frame_height, self.frame_width),  # Optimal batch size
                          (8, 3, self.frame_height, self.frame_width))  # Maximum shape
        config.add_optimization_profile(profile)

        # Build the engine
        serialized_engine = builder.build_serialized_network(network, config)
        if serialized_engine is None:
            raise RuntimeError("Failed to build TensorRT engine")

        runtime = trt.Runtime(logger)
        self.trt_engine = runtime.deserialize_cuda_engine(serialized_engine)
        self.context = self.trt_engine.create_execution_context()

        # Allocate buffers based on input and output shapes
        input_shape = (1, 3, self.frame_height, self.frame_width)
        output_shape = (1, 3, self.frame_height, self.frame_width)
        self.d_input = cuda.mem_alloc(trt.volume(input_shape) * np.dtype(np.float32).itemsize)
        self.d_output = cuda.mem_alloc(trt.volume(output_shape) * np.dtype(np.float32).itemsize)

        print(f"Model {self.model_path} converted to TensorRT")

    def trt_process(self, frame):
        # Normalize the frame
        frame = frame / 255.0  # Normalize to [0, 1]
        frame = frame.transpose((2, 0, 1))  # Change from HWC to CHW
        frame = np.expand_dims(frame, axis=0).astype(np.float32)  # Add batch dimension and convert to float32

        # Use multiple CUDA streams for overlapping data transfers and execution
        stream1 = cuda.Stream()
        stream2 = cuda.Stream()

        # Set tensor addresses
        self.context.set_binding_shape(0, frame.shape)
        bindings = [int(self.d_input), int(self.d_output)]

        # Copy data to input memory
        cuda.memcpy_htod_async(self.d_input, frame, stream1)

        # Run inference
        self.context.execute_async_v2(bindings=bindings, stream_handle=stream1.handle)

        # Copy output data from output memory
        output_data = np.empty((1, 3, self.frame_height, self.frame_width), dtype=np.float32)
        cuda.memcpy_dtoh_async(output_data, self.d_output, stream2)
        stream1.synchronize()
        stream2.synchronize()

        # Post-process output data as needed (e.g., convert to uint8, apply colormaps)
        output_data = np.clip(output_data, 0, 255).astype(np.uint8)

        if self.next_unit:
            return self.next_unit.process(output_data)
        return output_data
