# DeepSeek-OCR - Prompts and Resolution Modes

## Prompt Templates

DeepSeek-OCR supports various prompt templates for different OCR tasks.

### Document Processing Prompts

#### 1. Document to Markdown (Most Common)
```python
prompt = "<image>\n<|grounding|>Convert the document to markdown."
```
**Use for**: Documents, PDFs, scanned pages, reports
**Output**: Structured markdown with tables, headings, lists

#### 2. OCR with Layout Grounding
```python
prompt = "<image>\n<|grounding|>OCR this image."
```
**Use for**: General images with text, screenshots, diagrams
**Output**: Text with bounding box information

#### 3. Free OCR (No Layout)
```python
prompt = "<image>\nFree OCR."
```
**Use for**: Simple text extraction without layout
**Output**: Plain text only, no structure

#### 4. Figure Parsing
```python
prompt = "<image>\nParse the figure."
```
**Use for**: Charts, graphs, diagrams, flowcharts
**Output**: Structured description of visual elements

#### 5. Detailed Image Description
```python
prompt = "<image>\nDescribe this image in detail."
```
**Use for**: General image understanding
**Output**: Comprehensive description

#### 6. Text Localization
```python
prompt = "<image>\nLocate <|ref|>specific_text<|/ref|> in the image."
```
**Use for**: Finding specific text in documents
**Output**: Bounding box coordinates

## Resolution Modes

### Overview Table

| Mode | Resolution | Vision Tokens | Parameters | Use Case |
|------|-----------|---------------|------------|----------|
| **Tiny** | 512×512 | 64 | `base_size=512, image_size=512, crop_mode=False` | Fast processing, simple text |
| **Small** | 640×640 | 100 | `base_size=640, image_size=640, crop_mode=False` | Balanced speed/quality |
| **Base** | 1024×1024 | 256 | `base_size=1024, image_size=1024, crop_mode=False` | **Recommended for most tasks** |
| **Large** | 1280×1280 | 400 | `base_size=1280, image_size=1280, crop_mode=False` | High quality, complex documents |
| **Gundam** | n×640×640 + 1×1024×1024 | Variable | `base_size=1024, image_size=640, crop_mode=True` | **Dynamic resolution, large docs** |

### Mode Selection Guide

#### When to Use Tiny (512×512)
- ✅ Simple text extraction
- ✅ Low-resolution images
- ✅ Speed is critical
- ✅ Limited GPU memory (<6GB)
- ❌ Not for: Complex layouts, small text, tables

#### When to Use Small (640×640)
- ✅ Mobile app screenshots
- ✅ Medium-quality scans
- ✅ Balanced performance
- ✅ Moderate GPU memory (6-8GB)
- ❌ Not for: High-detail documents, charts

#### When to Use Base (1024×1024) - **Recommended**
- ✅ Most document types
- ✅ High-quality scans
- ✅ Tables and structured data
- ✅ Good balance of quality and speed
- ✅ GPU memory 10-12GB
- ❌ Not for: Very large documents

#### When to Use Large (1280×1280)
- ✅ Complex layouts
- ✅ Small text / fine details
- ✅ Scientific papers with formulas
- ✅ High-resolution scans
- ✅ GPU memory 16GB+
- ❌ Not for: Time-critical applications

#### When to Use Gundam (Dynamic)
- ✅ **Multi-page documents**
- ✅ **Very large images**
- ✅ **Variable content density**
- ✅ Automatic resolution adaptation
- ✅ GPU memory 12-20GB
- ❌ Not for: Small images, simple text

## Detailed Mode Configuration

### Tiny Mode
```python
res = model.infer(
    tokenizer,
    prompt="<image>\nFree OCR.",
    image_file='simple_text.jpg',
    base_size=512,
    image_size=512,
    crop_mode=False
)
```
**Performance**: ~50 tokens/s, ~4GB GPU
**Quality**: 3/5

### Small Mode
```python
res = model.infer(
    tokenizer,
    prompt="<image>\n<|grounding|>OCR this image.",
    image_file='screenshot.jpg',
    base_size=640,
    image_size=640,
    crop_mode=False
)
```
**Performance**: ~40 tokens/s, ~6GB GPU
**Quality**: 4/5

### Base Mode (Recommended)
```python
res = model.infer(
    tokenizer,
    prompt="<image>\n<|grounding|>Convert the document to markdown.",
    image_file='document.jpg',
    base_size=1024,
    image_size=1024,
    crop_mode=False
)
```
**Performance**: ~30 tokens/s, ~10GB GPU
**Quality**: 5/5

### Large Mode
```python
res = model.infer(
    tokenizer,
    prompt="<image>\n<|grounding|>Convert the document to markdown.",
    image_file='complex_document.jpg',
    base_size=1280,
    image_size=1280,
    crop_mode=False
)
```
**Performance**: ~20 tokens/s, ~16GB GPU
**Quality**: 5/5 (highest detail)

### Gundam Mode (Dynamic Resolution)
```python
res = model.infer(
    tokenizer,
    prompt="<image>\n<|grounding|>Convert the document to markdown.",
    image_file='large_document.jpg',
    base_size=1024,
    image_size=640,
    crop_mode=True  # Enable dynamic resolution
)
```
**Performance**: ~25 tokens/s, ~12-20GB GPU (varies)
**Quality**: 5/5 (adaptive)

**How Gundam works**:
1. Divides image into 640×640 patches
2. Processes each patch separately
3. Also processes full image at 1024×1024
4. Combines results for comprehensive understanding

## Prompt Engineering Tips

### 1. Use Grounding for Structured Output
```python
# ✅ Good - structured output with layout
prompt = "<image>\n<|grounding|>Convert the document to markdown."

# ❌ Less ideal - plain text only
prompt = "<image>\nFree OCR."
```

### 2. Be Specific About Task
```python
# ✅ Good - clear task
prompt = "<image>\n<|grounding|>OCR this invoice and extract fields."

# ❌ Vague
prompt = "<image>\nProcess this."
```

### 3. Match Prompt to Content Type
```python
# For documents
prompt = "<image>\n<|grounding|>Convert the document to markdown."

# For figures/charts
prompt = "<image>\nParse the figure."

# For general images
prompt = "<image>\nDescribe this image in detail."
```

### 4. Use Reference Tags for Localization
```python
# Find specific text
prompt = "<image>\nLocate <|ref|>Invoice Number<|/ref|> in the image."

# Output will include bounding boxes
```

## Performance vs Quality Trade-offs

```
Resolution   Speed        Quality      GPU Memory   Use Case
Tiny         ███████████  ██░░░        ██░░░        Quick scans
Small        ████████░░   ████░        ███░░        Screenshots
Base         ██████░░░    ██████       █████        Documents
Large        ████░░░░░    ███████      ███████      High detail
Gundam       █████░░░░    ███████      ██████       Large docs
```

## Example Workflows

### Workflow 1: Invoice Processing
```python
# Use Base mode with grounding for structured data
res = model.infer(
    tokenizer,
    prompt="<image>\n<|grounding|>Convert the document to markdown.",
    image_file='invoice.pdf',
    base_size=1024,
    image_size=1024,
    crop_mode=False
)
```

### Workflow 2: Large Report (Multi-page)
```python
# Use Gundam mode for dynamic resolution
res = model.infer(
    tokenizer,
    prompt="<image>\n<|grounding|>Convert the document to markdown.",
    image_file='report_page1.jpg',
    base_size=1024,
    image_size=640,
    crop_mode=True  # Handles large documents
)
```

### Workflow 3: Chart Extraction
```python
# Use Large mode for fine details
res = model.infer(
    tokenizer,
    prompt="<image>\nParse the figure.",
    image_file='chart.png',
    base_size=1280,
    image_size=1280,
    crop_mode=False
)
```

### Workflow 4: Fast Batch Processing
```python
# Use Small mode for speed
for img in image_list:
    res = model.infer(
        tokenizer,
        prompt="<image>\nFree OCR.",
        image_file=img,
        base_size=640,
        image_size=640,
        crop_mode=False
    )
```

## Special Tokens

| Token | ID | Purpose |
|-------|-----|---------|
| `<image>` | - | Image placeholder in prompt |
| `<\|grounding\|>` | - | Enable layout detection |
| `<\|ref\|>` | - | Start reference marker |
| `</\|ref\|>` | - | End reference marker |
| `<\|det\|>` | - | Start detection coordinates |
| `</\|det\|>` | - | End detection coordinates |
| `<td>` | 128821 | Table cell start |
| `</td>` | 128822 | Table cell end |

## Best Practices

1. **Start with Base mode** - Best balance for most tasks
2. **Use Gundam for large images** - Automatic handling of complex layouts
3. **Enable grounding for documents** - Better structured output
4. **Use free OCR for simple text** - Faster when layout not needed
5. **Match resolution to content** - Don't over-process simple images
6. **Test different prompts** - Small changes can improve results

## Next Steps

- **vllm_inference.md** - High-performance batch processing
- **code_examples.md** - Complete working examples
