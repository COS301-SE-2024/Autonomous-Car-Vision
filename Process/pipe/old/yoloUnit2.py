import cv2
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
from ultralytics import YOLO
from units import Unit
import os

class SegUnit(Unit):
    def __init__(self, model_name, frame_width, frame_height):
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

        self.trt_engine = None
        self.context = None

    def process(self, frame):
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
        onnx_model_path = self.model_path.replace('.pt', '.onnx')  # Define the path for the ONNX model

        # Export the model to ONNX format
        self.model.export(format='onnx')

        # Verify ONNX export
        if not os.path.exists(onnx_model_path):
            raise FileNotFoundError(f"ONNX model file '{onnx_model_path}' not found.")

        # Load the ONNX model and create a TensorRT engine
        logger = trt.Logger(trt.Logger.WARNING)  # Create a logger to capture warnings and errors from TensorRT
        builder = trt.Builder(logger)  # Create a builder for constructing the TensorRT engine
        network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))  # Create a network definition with explicit batch flag
        parser = trt.OnnxParser(network, logger)  # Create an ONNX parser to read the model into the network

        # Read the ONNX model file and parse it into the TensorRT network
        with open(onnx_model_path, 'rb') as model:
            if not parser.parse(model.read()):
                for error in range(parser.num_errors()):
                    print(parser.get_error(error))
                raise ValueError("Failed to parse the ONNX model")

        # Create a configuration for the builder
        config = builder.create_builder_config()
        config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30)  # Set memory limit for the builder to 1 GB

        # Set the optimization profile based on the provided frame sizes
        profile = builder.create_optimization_profile()
        profile.set_shape(network.get_input(0).name,
                          (1, 3, self.frame_height, self.frame_width),  # Minimum shape
                          (1, 3, self.frame_height, self.frame_width),  # Optimal shape
                          (1, 3, self.frame_height, self.frame_width))  # Maximum shape
        config.add_optimization_profile(profile)  # Add the optimization profile to the configuration

        # Build the engine and serialize it
        serialized_engine = builder.build_serialized_network(network, config)  # Serialize the network to create an engine
        runtime = trt.Runtime(logger)  # Create a runtime for deserializing the engine
        self.trt_engine = runtime.deserialize_cuda_engine(serialized_engine)  # Deserialize the engine
        self.context = self.trt_engine.create_execution_context()  # Create an execution context from the engine

        print(f"Model {self.model_path} converted to TensorRT")

    def trt_process(self, frame):
        # Normalize the frame
        frame = frame / 255.0  # Normalize to [0, 1]
        frame = frame.transpose((2, 0, 1))  # Change from HWC (Height, Width, Channels) to CHW (Channels, Height, Width)
        frame = np.expand_dims(frame, axis=0).astype(np.float32)  # Add batch dimension and convert to float32

        # Allocate memory for inputs and outputs (TensorRT-specific)
        input_shape = frame.shape  # Get the shape of the input frame
        output_shape = (1, 3, self.frame_height, self.frame_width)  # Define the output shape
        d_input = cuda.mem_alloc(trt.volume(input_shape) * np.dtype(np.float32).itemsize)  # Allocate device memory for input
        d_output = cuda.mem_alloc(trt.volume(output_shape) * np.dtype(np.float32).itemsize)  # Allocate device memory for output
        stream = cuda.Stream()  # Create a CUDA stream for asynchronous execution

        # Set tensor addresses
        self.context.set_binding_shape(0, input_shape)  # Set the shape of the input tensor
        bindings = [int(d_input), int(d_output)]  # Create a list of input and output bindings

        # Copy data to input memory
        cuda.memcpy_htod_async(d_input, frame, stream)  # Copy input data to the device memory asynchronously

        # Run inference
        self.context.execute_async_v3(bindings=bindings, stream_handle=stream.handle)  # Execute inference asynchronously

        # Copy output data from output memory
        output_data = np.empty(output_shape, dtype=np.float32)  # Create an empty array for the output data
        cuda.memcpy_dtoh_async(output_data, d_output, stream)  # Copy output data from the device memory asynchronously
        stream.synchronize()  # Synchronize the stream to ensure all operations are complete

        # Post-process output data as needed (e.g., convert to uint8, apply colormaps)
        output_data = np.clip(output_data, 0, 255).astype(np.uint8)  # Clip the output data to [0, 255] and convert to uint8

        if self.next_unit:
            return self.next_unit.process(output_data)  # Pass the output to the next unit in the pipeline if it exists
        return output_data  # Return the processed output data
