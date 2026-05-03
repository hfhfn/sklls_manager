# DeepSeek-OCR - Installation Guide

## System Requirements

- **CUDA Version**: 11.8+
- **Python Version**: 3.12.9 (recommended) or 3.8+
- **PyTorch Version**: 2.6.0
- **GPU**: NVIDIA GPU with CUDA support (A100 recommended for production)
- **Memory**: At least 16GB GPU memory for base model

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/deepseek-ai/DeepSeek-OCR.git
cd DeepSeek-OCR
```

### 2. Create Conda Environment

```bash
conda create -n deepseek-ocr python=3.12.9 -y
conda activate deepseek-ocr
```

### 3. Install PyTorch

```bash
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu118
```

### 4. Install vLLM

Download the vLLM wheel file from [GitHub releases](https://github.com/vllm-project/vllm/releases/tag/v0.8.5):

```bash
pip install vllm-0.8.5+cu118-cp38-abi3-manylinux1_x86_64.whl
```

**Note**: If using both vLLM and Transformers in the same environment, you can ignore version conflicts like:
```
vllm 0.8.5+cu118 requires transformers>=4.51.1
```

### 5. Install Additional Dependencies

```bash
pip install -r requirements.txt
pip install flash-attn==2.7.3 --no-build-isolation
```

## Using Upstream vLLM (Newer Version)

As of October 2025, DeepSeek-OCR is officially supported in upstream vLLM:

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install from nightly build (until v0.11.1 release)
uv pip install -U vllm --pre --extra-index-url https://wheels.vllm.ai/nightly
```

## Verification

Test your installation:

```python
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")

from transformers import AutoModel, AutoTokenizer
print("Transformers installed successfully")

try:
    from vllm import LLM
    print("vLLM installed successfully")
except ImportError:
    print("vLLM not installed (optional)")
```

## Troubleshooting

### Issue: CUDA Version Mismatch
```bash
# Set CUDA path if using CUDA 11.8
export TRITON_PTXAS_PATH="/usr/local/cuda-11.8/bin/ptxas"
```

### Issue: Flash Attention Installation Failed
```bash
# Try without --no-build-isolation
pip install flash-attn==2.7.3

# Or use pre-built wheels
pip install flash-attn --find-links https://github.com/Dao-AILab/flash-attention/releases
```

### Issue: Out of Memory
- Use smaller resolution modes (Tiny or Small)
- Reduce batch size
- Use CPU offloading (slower but works)
- Upgrade to GPU with more memory

## Next Steps

After installation, proceed to:
- **transformers_inference.md** - Basic inference with Transformers
- **vllm_inference.md** - High-performance inference with vLLM
