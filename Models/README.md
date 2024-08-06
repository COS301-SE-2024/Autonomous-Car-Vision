# Setting Up the Models Environment

This guide will walk you through setting up a virtual environment for the Models project, installing necessary dependencies, and configuring PyTorch with CUDA support for optimized performance.

## Step 1: Navigate to the Models Directory

Open your terminal and navigate to the Models directory using the `cd` command:

```bash
cd Models
```

## Step 2: Setup the virtual environment and install the necessary dependencies

Create the virtual environment:

```bash
python -m venv modelsVenv
```
Activate the Virtual Environment:

- On wondows:

    ```bash
    modelsVenv\Scripts\activate
    ```

- On Linux:

    ```bash
    source modelsVenv/bin/activate
    ```
Install Ultralytics:

```bash
pip install ultralytics
```

Install imageio:

```bash
pip install imageio
pip install imageio[ffmpeg]
```

Uninstall Existing PyTorch Packages:

```bash
pip uninstall -y torch torchvision torchaudio
```

Install PyTorch with CUDA Support:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Install CUDA Toolkit

Download and install the CUDA Toolkit from the official NVIDIA website. Visit the link below and follow the installation instructions for your operating system:

[CUDO Toolkit download](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11)

Make sure to follow the instructions carefully to ensure CUDA is installed correctly and is compatible with your GPU