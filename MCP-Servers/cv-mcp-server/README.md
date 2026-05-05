# Computer Vision MCP Server

A Model Context Protocol (MCP) server that provides comprehensive computer vision capabilities including object detection, image segmentation, captioning, classification, and more.

## 🚀 Features

This CV MCP server provides the following computer vision tools:

### 🔍 Object Detection
- **detect_objects**: Detect objects using YOLOv8 with configurable model sizes
- Returns bounding boxes, class labels, and confidence scores

### 🎨 Image Segmentation
- **segment_image**: Semantic segmentation using DeepLabV3, Mask R-CNN, or SAM
- Outputs labeled regions and optional visualizations

### 💬 Image Captioning
- **caption_image**: Generate natural language descriptions using BLIP
- Configurable caption length and generation quality

### 🏷️ Image Classification
- **classify_image**: Classify images using ResNet, Vision Transformer, or EfficientNet
- Returns top-k predictions with confidence scores

### 👤 Face Detection
- **detect_faces**: Detect faces with bounding boxes and landmarks
- Facial landmark detection for advanced analysis

### 🧬 Feature Extraction
- **extract_features**: Extract deep feature vectors for similarity search
- Useful for image retrieval and clustering

### 🤸 Pose Estimation
- **pose_estimation**: Estimate human pose keypoints
- Detects body joints and skeletal structure

### 📏 Depth Estimation
- **depth_estimation**: Monocular depth estimation from RGB images
- Returns depth maps with optional colorization

### 🎭 Style Transfer
- **style_transfer**: Apply artistic styles to images
- Neural style transfer with adjustable strength

### ✂️ Background Removal
- **remove_background**: Remove or replace image backgrounds
- Support for transparent or custom colored backgrounds

## 📋 Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (optional, but recommended for better performance)

## 📥 Installation

### 1. Install Dependencies

```bash
# Install using pip
pip install -e .

# Or install from pyproject.toml
pip install torch torchvision transformers pillow numpy opencv-python ultralytics
pip install mcp
```

### 2. Configure Environment

Create or update the `.env` file with your settings:

```bash
# Optional: Set custom model cache directory
HF_HOME=/path/to/cache

# Optional: Hugging Face API token for private models
HF_TOKEN=your_huggingface_token_here

# Optional: Device configuration (cpu, cuda, mps)
DEVICE=cpu  # or cuda, mps
```

## 🎯 Usage

### Running the MCP Server

```bash
# Run the server
python cv_mcp_server.py
```

### Using with MCP Clients

The server communicates via stdin/stdout following the MCP protocol. Configure your MCP client to connect to this server.

Example configuration for Claude Desktop or other MCP clients:

```json
{
  "mcpServers": {
    "cv-server": {
      "command": "python",
      "args": ["path/to/cv_mcp_server.py"],
      "env": {
        "DEVICE": "cuda"
      }
    }
  }
}
```

### Example Tool Usage

#### Object Detection
```json
{
  "tool": "detect_objects",
  "arguments": {
    "image_path": "/path/to/image.jpg",
    "confidence_threshold": 0.5,
    "model_size": "m"
  }
}
```

#### Image Captioning
```json
{
  "tool": "caption_image",
  "arguments": {
    "image_path": "/path/to/image.jpg",
    "max_length": 50,
    "num_beams": 4
  }
}
```

#### Image Segmentation
```json
{
  "tool": "segment_image",
  "arguments": {
    "image_path": "/path/to/image.jpg",
    "output_path": "/path/to/output.png",
    "model_type": "deeplabv3"
  }
}
```

## 🛠️ Development

### Project Structure

```
cv-mcp-server/
├── cv_mcp_server.py      # Main MCP server
├── cv_tools.py            # CV tool implementations
├── pyproject.toml         # Project configuration
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── tools/                # Individual tool modules
    ├── paths.py          # Tool paths configuration
    └── cv-api/           # CV tool implementations
        ├── detect_objects.py
        ├── segment_image.py
        ├── caption_image.py
        ├── classify_image.py
        ├── detect_faces.py
        ├── extract_features.py
        ├── pose_estimation.py
        ├── depth_estimation.py
        ├── style_transfer.py
        └── remove_background.py
```

### Adding New Tools

1. Implement the tool function in `cv_tools.py`
2. Add the tool definition in `cv_mcp_server.py` TOOLS list
3. Map the function in TOOL_FUNCTIONS dictionary
4. Optionally create a dedicated module in `tools/cv-api/`

## 🔧 Configuration

### Model Selection

The server supports multiple models for various tasks:

- **Object Detection**: YOLOv8 (nano, small, medium, large, extra-large)
- **Segmentation**: DeepLabV3, Mask R-CNN, SAM
- **Classification**: ResNet50, Vision Transformer, EfficientNet
- **Captioning**: BLIP
- **Depth Estimation**: DPT (Dense Prediction Transformer)

### Device Configuration

The server automatically detects the best available device (CUDA > MPS > CPU). You can override this by setting the `DEVICE` environment variable:

```bash
export DEVICE=cuda  # Use NVIDIA GPU
export DEVICE=mps   # Use Apple Silicon GPU
export DEVICE=cpu   # Use CPU only
```

### Model Caching

Models are automatically downloaded and cached. Set `HF_HOME` to specify a custom cache directory:

```bash
export HF_HOME=/path/to/model/cache
```

## 📊 Performance Tips

1. **Use GPU**: Install CUDA-enabled PyTorch for significantly faster inference
2. **Model Size**: Use smaller models (e.g., YOLOv8n) for faster processing
3. **Batch Processing**: Process multiple images in batches when possible
4. **Cache Models**: Pre-download models to avoid delays on first use

## 🐛 Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'torch'**
- Install PyTorch: `pip install torch torchvision`

**CUDA out of memory**
- Use smaller models or switch to CPU: `export DEVICE=cpu`

**Model download fails**
- Check internet connection
- Set HuggingFace token if accessing private models: `export HF_TOKEN=your_token`

**Slow inference**
- Ensure CUDA is properly installed for GPU acceleration
- Use smaller model variants for faster processing

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📚 References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [PyTorch Vision](https://pytorch.org/vision/)

## 🔗 Related Projects

- [filesystem-mcp-server](../filesystem-mcp-server) - File system operations MCP server
- [xml-mcp-server](../xml-mcp-server) - XML processing MCP server
- [postman-mcp-server](../postman-mcp-server) - API testing MCP server
