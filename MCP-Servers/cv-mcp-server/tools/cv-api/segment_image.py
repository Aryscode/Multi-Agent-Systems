"""
Image Segmentation Tool

Performs semantic segmentation on images.
Returns segmented regions with labels.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute semantic segmentation on an image.
    
    Args:
        args: Dictionary containing:
            - image_path: Path to the input image
            - output_path: Path to save segmented image (optional)
            - model_type: Segmentation model type (default: 'deeplabv3')
    
    Returns:
        Segmentation results with labeled regions
    """
    from cv_tools import segment_image
    return await segment_image(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "segment_image",
            "description": "Perform semantic segmentation on an image. Returns segmented regions with labels and optionally saves a visualization.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional path to save the segmented image visualization"
                    },
                    "model_type": {
                        "type": "string",
                        "description": "Segmentation model: 'sam' (Segment Anything), 'deeplabv3', or 'maskrcnn'. Default: 'deeplabv3'",
                        "enum": ["sam", "deeplabv3", "maskrcnn"],
                        "default": "deeplabv3"
                    }
                },
                "required": ["image_path"]
            }
        }
    }
}
