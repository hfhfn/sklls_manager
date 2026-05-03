# DeepSeek-OCR - Transformers Inference

## Basic Usage

### Simple Example

```python
from transformers import AutoModel, AutoTokenizer
import torch
import os

os.environ["CUDA_VISIBLE_DEVICES"] = '0'

model_name = 'deepseek-ai/DeepSeek-OCR'

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name,
    _attn_implementation='flash_attention_2',
    trust_remote_code=True,
    use_safetensors=True
)
model = model.eval().cuda().to(torch.bfloat16)

# Prepare input
prompt = "<image>\n<|grounding|>Convert the document to markdown."
image_file = 'your_image.jpg'
output_path = 'your/output/dir'

# Run inference
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

## Model.infer() API

### Parameters

```python
model.infer(
    tokenizer,          # AutoTokenizer instance
    prompt='',          # Text prompt with <image> placeholder
    image_file='',      # Path to input image
    output_path='',     # Directory for output files
    base_size=1024,     # Base resolution (512/640/1024/1280)
    image_size=640,     # Image patch size
    crop_mode=False,    # Enable dynamic resolution (Gundam mode)
    save_results=False, # Save output files
    test_compress=False # Test compression mode
)
```

### Resolution Mode Configuration

#### Tiny Mode (Fast, Low Quality)
```python
base_size = 512
image_size = 512
crop_mode = False
# Vision tokens: 64
```

#### Small Mode (Balanced)
```python
base_size = 640
image_size = 640
crop_mode = False
# Vision tokens: 100
```

#### Base Mode (Recommended)
```python
base_size = 1024
image_size = 1024
crop_mode = False
# Vision tokens: 256
```

#### Large Mode (High Quality)
```python
base_size = 1280
image_size = 1280
crop_mode = False
# Vision tokens: 400
```

#### Gundam Mode (Dynamic Resolution)
```python
base_size = 1024
image_size = 640
crop_mode = True
# Vision tokens: Variable (n×100 + 256)
```

## Complete Working Example

```python
from transformers import AutoModel, AutoTokenizer
import torch
import os

# Setup
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
model_name = 'deepseek-ai/DeepSeek-OCR'

# Load model
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name,
    _attn_implementation='flash_attention_2',
    trust_remote_code=True,
    use_safetensors=True
)
model = model.eval().cuda().to(torch.bfloat16)

# Example 1: Document to Markdown
result = model.infer(
    tokenizer,
    prompt="<image>\n<|grounding|>Convert the document to markdown.",
    image_file='document.jpg',
    output_path='./output',
    base_size=1024,
    image_size=640,
    crop_mode=True,
    save_results=True,
    test_compress=True
)
print("Markdown output:", result)

# Example 2: Free OCR (No Layout)
result = model.infer(
    tokenizer,
    prompt="<image>\nFree OCR.",
    image_file='text_image.jpg',
    output_path='./output',
    base_size=1024,
    image_size=1024,
    crop_mode=False
)
print("OCR output:", result)

# Example 3: Parse Figure
result = model.infer(
    tokenizer,
    prompt="<image>\nParse the figure.",
    image_file='chart.jpg',
    output_path='./output',
    base_size=1280,
    image_size=1280,
    crop_mode=False
)
print("Figure description:", result)
```

## Using the Repository Script

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-hf
python run_dpsk_ocr.py
```

Edit `run_dpsk_ocr.py` to customize:
- `prompt`: Change the OCR task
- `image_file`: Input image path
- `output_path`: Output directory
- `base_size`, `image_size`, `crop_mode`: Resolution settings

## Performance Tips

1. **Use bfloat16**: `model.to(torch.bfloat16)` for better performance
2. **Enable Flash Attention**: `_attn_implementation='flash_attention_2'`
3. **Use crop_mode=True**: For large documents (dynamic resolution)
4. **Batch Processing**: Process multiple images in a loop
5. **GPU Selection**: Set `CUDA_VISIBLE_DEVICES` to select GPU

## Memory Requirements

| Resolution Mode | GPU Memory | Typical Speed |
|----------------|------------|---------------|
| Tiny (512×512) | ~4GB | ~50 tokens/s |
| Small (640×640) | ~6GB | ~40 tokens/s |
| Base (1024×1024) | ~10GB | ~30 tokens/s |
| Large (1280×1280) | ~16GB | ~20 tokens/s |
| Gundam (dynamic) | ~12-20GB | ~25 tokens/s |

## Common Issues

### Issue: Model Not Found
```python
# Download model first
from huggingface_hub import snapshot_download
snapshot_download(repo_id="deepseek-ai/DeepSeek-OCR")
```

### Issue: CUDA Out of Memory
- Reduce resolution (use Tiny or Small mode)
- Use CPU inference (very slow):
  ```python
  model = model.eval().cpu().to(torch.bfloat16)
  ```

### Issue: Slow Inference
- Enable flash attention
- Use vLLM instead (see vllm_inference.md)
- Use GPU with better compute capability

## Next Steps

For production deployments with higher throughput:
- **vllm_inference.md** - High-performance batch inference
