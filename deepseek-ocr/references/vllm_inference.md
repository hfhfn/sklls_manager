# DeepSeek-OCR - vLLM Inference (High Performance)

## Overview

vLLM provides 2-3x faster inference compared to Transformers, with support for:
- Batch processing (~2500 tokens/s on A100)
- Streaming output
- Concurrent PDF processing
- Efficient memory management

## Installation

```bash
# Install vLLM 0.8.5
pip install vllm-0.8.5+cu118-cp38-abi3-manylinux1_x86_64.whl

# Or use upstream vLLM (newer, October 2025+)
uv pip install -U vllm --pre --extra-index-url https://wheels.vllm.ai/nightly
```

## Basic Usage with Upstream vLLM

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
image_1 = Image.open("path/to/your/image_1.png").convert("RGB")
image_2 = Image.open("path/to/your/image_2.png").convert("RGB")
prompt = "<image>\nFree OCR."

model_input = [
    {
        "prompt": prompt,
        "multi_modal_data": {"image": image_1}
    },
    {
        "prompt": prompt,
        "multi_modal_data": {"image": image_2}
    }
]

# Configure sampling
sampling_param = SamplingParams(
    temperature=0.0,
    max_tokens=8192,
    # ngram logit processor args (prevents repetition)
    extra_args=dict(
        ngram_size=30,
        window_size=90,
        whitelist_token_ids={128821, 128822},  # whitelist: <td>, </td>
    ),
    skip_special_tokens=False,
)

# Generate output
model_outputs = llm.generate(model_input, sampling_param)

# Print results
for output in model_outputs:
    print(output.outputs[0].text)
```

## Repository Scripts

### 1. Image Processing with Streaming

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-vllm

# Edit config.py to set paths
python run_dpsk_ocr_image.py
```

**Features**:
- Streaming output (real-time results)
- Bounding box visualization
- Automatic image extraction from documents
- Markdown output with embedded images

### 2. PDF Processing with Concurrency

```bash
python run_dpsk_ocr_pdf.py
```

**Performance**: ~2500 tokens/s on A100-40G with concurrent processing

### 3. Batch Evaluation

```bash
python run_dpsk_ocr_eval_batch.py
```

For benchmark evaluation on multiple documents.

## Configuration (config.py)

```python
# Model path
MODEL_PATH = "deepseek-ai/DeepSeek-OCR"

# Input/Output paths
INPUT_PATH = "path/to/input/image.jpg"
OUTPUT_PATH = "path/to/output/directory"

# Prompt
PROMPT = "<image>\n<|grounding|>Convert the document to markdown."

# Cropping mode (Gundam dynamic resolution)
CROP_MODE = True
```

## Advanced: Async Streaming Example

```python
import asyncio
import torch
import os

os.environ['VLLM_USE_V1'] = '0'
os.environ["CUDA_VISIBLE_DEVICES"] = '0'

from vllm import AsyncLLMEngine, SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.model_executor.models.registry import ModelRegistry
from deepseek_ocr import DeepseekOCRForCausalLM
from PIL import Image

# Register custom model
ModelRegistry.register_model("DeepseekOCRForCausalLM", DeepseekOCRForCausalLM)

async def stream_generate(image=None, prompt=''):
    # Configure engine
    engine_args = AsyncEngineArgs(
        model="deepseek-ai/DeepSeek-OCR",
        hf_overrides={"architectures": ["DeepseekOCRForCausalLM"]},
        block_size=256,
        max_model_len=8192,
        enforce_eager=False,
        trust_remote_code=True,
        tensor_parallel_size=1,
        gpu_memory_utilization=0.75,
    )
    engine = AsyncLLMEngine.from_engine_args(engine_args)

    # Configure logits processors (prevent n-gram repetition)
    from process.ngram_norepeat import NoRepeatNGramLogitsProcessor
    logits_processors = [
        NoRepeatNGramLogitsProcessor(
            ngram_size=30,
            window_size=90,
            whitelist_token_ids={128821, 128822}  # <td>, </td>
        )
    ]

    sampling_params = SamplingParams(
        temperature=0.0,
        max_tokens=8192,
        logits_processors=logits_processors,
        skip_special_tokens=False,
    )

    request_id = f"request-{int(time.time())}"
    printed_length = 0

    # Prepare request
    request = {
        "prompt": prompt,
        "multi_modal_data": {"image": image}
    }

    # Stream output
    async for request_output in engine.generate(request, sampling_params, request_id):
        if request_output.outputs:
            full_text = request_output.outputs[0].text
            new_text = full_text[printed_length:]
            print(new_text, end='', flush=True)
            printed_length = len(full_text)
            final_output = full_text

    print('\n')
    return final_output

# Run
image = Image.open("document.jpg").convert('RGB')
prompt = "<image>\n<|grounding|>Convert the document to markdown."
result = asyncio.run(stream_generate(image, prompt))
```

## Image Processing Features

### Load Image with EXIF Handling

```python
from PIL import Image, ImageOps

def load_image(image_path):
    try:
        image = Image.open(image_path)
        # Correct orientation based on EXIF data
        corrected_image = ImageOps.exif_transpose(image)
        return corrected_image
    except Exception as e:
        print(f"Error: {e}")
        return Image.open(image_path)
```

### Image Preprocessing

```python
from process.image_process import DeepseekOCRProcessor

# Tokenize images with cropping
processor = DeepseekOCRProcessor()
image_features = processor.tokenize_with_images(
    images=[image],
    bos=True,
    eos=True,
    cropping=CROP_MODE
)
```

## N-Gram Repetition Prevention

The logits processor prevents repetitive text:

```python
logits_processors = [
    NoRepeatNGramLogitsProcessor(
        ngram_size=30,      # Size of n-gram to check
        window_size=90,     # Context window
        whitelist_token_ids={128821, 128822}  # Allow these tokens to repeat
    )
]
```

**Whitelist tokens**:
- `128821`: `<td>` (table cell start)
- `128822`: `</td>` (table cell end)

These are allowed to repeat for proper table formatting.

## Performance Optimization

### Engine Configuration

```python
engine_args = AsyncEngineArgs(
    model="deepseek-ai/DeepSeek-OCR",
    block_size=256,                    # KV cache block size
    max_model_len=8192,                # Max sequence length
    enforce_eager=False,               # Use CUDA graphs
    trust_remote_code=True,
    tensor_parallel_size=1,            # Number of GPUs
    gpu_memory_utilization=0.75,       # GPU memory fraction
)
```

### Batch Processing

```python
# Process multiple images in one batch
model_input = [
    {"prompt": prompt, "multi_modal_data": {"image": img1}},
    {"prompt": prompt, "multi_modal_data": {"image": img2}},
    {"prompt": prompt, "multi_modal_data": {"image": img3}},
]

outputs = llm.generate(model_input, sampling_param)
```

## Output Post-Processing

### Extract and Save Images from Documents

```python
import re

def re_match(text):
    """Extract grounding references from output"""
    pattern = r'(<\|ref\|>(.*?)<\|/ref\|><\|det\|>(.*?)<\|/det\|>)'
    matches = re.findall(pattern, text, re.DOTALL)

    matches_image = []
    matches_other = []
    for a_match in matches:
        if '<|ref|>image<|/ref|>' in a_match[0]:
            matches_image.append(a_match[0])
        else:
            matches_other.append(a_match[0])

    return matches, matches_image, matches_other

# Use in output processing
matches_ref, matches_images, matches_other = re_match(output_text)

# Replace image references with markdown links
for idx, match_image in enumerate(matches_images):
    output_text = output_text.replace(match_image, f'![](images/{idx}.jpg)\n')
```

## Memory Requirements

| Configuration | GPU Memory | Throughput |
|--------------|------------|------------|
| Single image (Base) | ~8GB | ~30 tokens/s |
| Batch size 4 (Base) | ~20GB | ~100 tokens/s |
| Concurrent PDF (A100) | ~35GB | ~2500 tokens/s |
| Tensor parallel (2×A100) | 2×40GB | ~5000 tokens/s |

## Troubleshooting

### Issue: CUDA Out of Memory
```python
# Reduce GPU memory utilization
gpu_memory_utilization=0.5
```

### Issue: Slow Streaming
```python
# Enable CUDA graphs
enforce_eager=False
```

### Issue: Repetitive Output
```python
# Increase n-gram size
ngram_size=50
window_size=150
```

## Next Steps

- **prompts_and_modes.md** - Prompt engineering and resolution modes
- **code_examples.md** - Complete working examples
