---
name: deepseek-ocr
description: DeepSeek OCR - Advanced optical character recognition using deep learning. Use for OCR tasks, document analysis, text extraction, and vision-language models.
---

# DeepSeek-OCR Skill

Comprehensive assistance with DeepSeek-OCR, an advanced OCR model for document understanding and text extraction.

## When to Use This Skill

This skill should be triggered when:
- Working with optical character recognition (OCR) tasks
- Processing documents, PDFs, or images for text extraction
- Converting documents to markdown format
- Implementing vision-language models for document understanding
- Extracting structured data from documents or forms
- Using deep learning for text recognition and layout analysis

## Quick Reference

### Installation

```bash
# Clone repository
git clone https://github.com/deepseek-ai/DeepSeek-OCR.git

# Create conda environment
conda create -n deepseek-ocr python=3.12.9 -y
conda activate deepseek-ocr

# Install PyTorch
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu118

# Install vLLM (download wheel from GitHub releases)
pip install vllm-0.8.5+cu118-cp38-abi3-manylinux1_x86_64.whl

# Install dependencies
pip install -r requirements.txt
pip install flash-attn==2.7.3 --no-build-isolation
```

### Transformers Inference (Quick Start)

```python
from transformers import AutoModel, AutoTokenizer
import torch

model_name = 'deepseek-ai/DeepSeek-OCR'

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name,
    _attn_implementation='flash_attention_2',
    trust_remote_code=True,
    use_safetensors=True
)
model = model.eval().cuda().to(torch.bfloat16)

# Run inference
prompt = "<image>\n<|grounding|>Convert the document to markdown."
image_file = 'your_image.jpg'
output_path = 'your/output/dir'

res = model.infer(
    tokenizer,
    prompt=prompt,
    image_file=image_file,
    output_path=output_path,
    base_size=1024,
    image_size=640,
    crop_mode=True,
    save_results=True,
    test_compress=True
)
```

### vLLM Inference (High Performance)

```python
from vllm import LLM, SamplingParams
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor
from PIL import Image

# Create model instance
llm = LLM(
    model="deepseek-ai/DeepSeek-OCR",
    enable_prefix_caching=False,
    mm_processor_cache_gb=0,
    logits_processors=[NGramPerReqLogitsProcessor]
)

# Prepare input
image = Image.open("path/to/your/image.png").convert("RGB")
prompt = "<image>\nFree OCR."

model_input = [{
    "prompt": prompt,
    "multi_modal_data": {"image": image}
}]

sampling_param = SamplingParams(
    temperature=0.0,
    max_tokens=8192,
    extra_args=dict(
        ngram_size=30,
        window_size=90,
        whitelist_token_ids={128821, 128822},  # whitelist: <td>, </td>
    ),
    skip_special_tokens=False,
)

# Generate output
model_outputs = llm.generate(model_input, sampling_param)
print(model_outputs[0].outputs[0].text)
```

### Common Prompts

```python
# Document to markdown conversion
"<image>\n<|grounding|>Convert the document to markdown."

# General OCR for images
"<image>\n<|grounding|>OCR this image."

# Free OCR without layouts
"<image>\nFree OCR."

# Parse figures in documents
"<image>\nParse the figure."

# Detailed image description
"<image>\nDescribe this image in detail."

# Locate specific text
"<image>\nLocate <|ref|>xxxx<|/ref|> in the image."
```

### Resolution Modes

| Mode | Resolution | Vision Tokens | Use Case |
|------|-----------|---------------|----------|
| Tiny | 512×512 | 64 | Fast processing, simple text |
| Small | 640×640 | 100 | Balanced speed/quality |
| Base | 1024×1024 | 256 | Standard quality (recommended) |
| Large | 1280×1280 | 400 | High quality, complex documents |
| Gundam | n×640×640 + 1×1024×1024 | Variable | Dynamic resolution, large documents |

### Model Parameters by Mode

```python
# Tiny mode
base_size = 512, image_size = 512, crop_mode = False

# Small mode
base_size = 640, image_size = 640, crop_mode = False

# Base mode (default)
base_size = 1024, image_size = 1024, crop_mode = False

# Large mode
base_size = 1280, image_size = 1280, crop_mode = False

# Gundam mode (dynamic resolution)
base_size = 1024, image_size = 640, crop_mode = True
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **installation.md** - Installation and setup guide
- **transformers_inference.md** - Using with Transformers library
- **vllm_inference.md** - High-performance vLLM inference
- **prompts_and_modes.md** - Prompt templates and resolution modes
- **code_examples.md** - Complete code examples from the repository
- **api_reference.md** - Model API and parameters

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the installation.md and transformers_inference.md reference files for basic setup and usage.

### For Production Deployment
Review vllm_inference.md for high-performance batch processing and PDF handling.

### For Custom Prompts
See prompts_and_modes.md for different prompt templates and when to use each resolution mode.

### For Code Examples
The code_examples.md file contains complete working examples from the official repository.

## Key Features

1. **Multiple Resolution Modes** - From 64 to 400+ vision tokens depending on quality needs
2. **Dynamic Resolution (Gundam)** - Automatic handling of large documents
3. **Document to Markdown** - Convert documents to structured markdown format
4. **Layout Understanding** - Grounded detection with bounding boxes
5. **High Performance** - vLLM support for ~2500 tokens/s on A100
6. **Batch Processing** - Handle multiple images/PDFs concurrently
7. **Flash Attention 2** - Optimized memory and speed with flash-attn

## Resources

### Model Links
- **Hugging Face**: https://huggingface.co/deepseek-ai/DeepSeek-OCR
- **Paper**: https://arxiv.org/abs/2510.18234
- **GitHub**: https://github.com/deepseek-ai/DeepSeek-OCR

### references/
Organized documentation extracted from the repository. These files contain:
- Complete installation instructions
- Inference examples with both Transformers and vLLM
- Prompt engineering guidelines
- Performance optimization tips
- Code samples from official examples

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, sample images, or example projects here.

## Notes

- This skill was created from the official DeepSeek-OCR repository
- Requires CUDA 11.8+ and PyTorch 2.6.0
- Flash Attention 2 is required for optimal performance
- vLLM 0.8.5+ recommended for production use
- Model supports both CPU and GPU inference (GPU strongly recommended)

## Citation

```bibtex
@article{wei2025deepseek,
  title={DeepSeek-OCR: Contexts Optical Compression},
  author={Wei, Haoran and Sun, Yaofeng and Li, Yukun},
  journal={arXiv preprint arXiv:2510.18234},
  year={2025}
}
```

## Updating

To refresh this skill with updated code:
1. Pull the latest changes from the repository
2. Review new examples and features
3. Update the skill documentation accordingly
