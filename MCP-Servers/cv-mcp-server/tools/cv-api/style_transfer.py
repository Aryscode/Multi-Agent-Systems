"""
Style Transfer Tool

Applies artistic style transfer to images.
Transfers the style of one image to the content of another.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply style transfer to an image.
    
    Args:
        args: Dictionary containing:
            - content_image: Path to content image
            - style_image: Path to style image
            - output_path: Path to save styled image
            - strength: Style strength (0-1, default: 0.5)
    
    Returns:
        Style transfer results
    """
    from cv_tools import style_transfer
    return await style_transfer(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "style_transfer",
            "description": "Apply artistic style transfer to an image. Transfers the artistic style of one image to the content of another image.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content_image": {
                        "type": "string",
                        "description": "Path to the content image (the image to be stylized)"
                    },
                    "style_image": {
                        "type": "string",
                        "description": "Path to the style image (the artistic style to apply)"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path to save the stylized output image"
                    },
                    "strength": {
                        "type": "number",
                        "description": "Style strength/intensity (0-1). Higher values apply stronger stylization. Default: 0.5",
                        "default": 0.5
                    }
                },
                "required": ["content_image", "style_image", "output_path"]
            }
        }
    }
}
