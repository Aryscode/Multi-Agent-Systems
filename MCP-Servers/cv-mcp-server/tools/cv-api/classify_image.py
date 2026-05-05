"""
Image Classification Tool

Classifies images into predefined categories.
Uses pre-trained models like ResNet, ViT, or EfficientNet.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify an image into categories.
    
    Args:
        args: Dictionary containing:
            - image_path: Path to the input image
            - top_k: Number of top predictions (default: 5)
            - model_name: Model to use (default: 'resnet50')
    
    Returns:
        Top-k classification predictions with labels and scores
    """
    from cv_tools import classify_image
    return await classify_image(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "classify_image",
            "description": "Classify an image into predefined categories (ImageNet classes). Returns top-k predictions with labels and confidence scores.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of top predictions to return. Default: 5",
                        "default": 5
                    },
                    "model_name": {
                        "type": "string",
                        "description": "Classification model: 'resnet50', 'vit' (Vision Transformer), or 'efficientnet'. Default: 'resnet50'",
                        "enum": ["resnet50", "vit", "efficientnet"],
                        "default": "resnet50"
                    }
                },
                "required": ["image_path"]
            }
        }
    }
}
