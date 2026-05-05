"""
Feature Extraction Tool

Extracts deep feature vectors from images using CNNs.
Useful for similarity search and image retrieval.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract deep features from an image.
    
    Args:
        args: Dictionary containing:
            - image_path: Path to the input image
            - layer: Layer to extract features from (default: 'pool')
    
    Returns:
        Feature vector representing the image
    """
    from cv_tools import extract_features
    return await extract_features(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "extract_features",
            "description": "Extract deep feature vectors from an image using a pre-trained CNN. Useful for image similarity and retrieval tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "layer": {
                        "type": "string",
                        "description": "Network layer to extract features from: 'pool' (global pooling), 'conv' (convolutional), or 'fc' (fully connected). Default: 'pool'",
                        "enum": ["pool", "conv", "fc"],
                        "default": "pool"
                    }
                },
                "required": ["image_path"]
            }
        }
    }
}
