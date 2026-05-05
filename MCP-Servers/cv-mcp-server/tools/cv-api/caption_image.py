"""
Image Captioning Tool

Generates natural language descriptions for images.
Uses BLIP model for image-to-text generation.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a caption for an image.
    
    Args:
        args: Dictionary containing:
            - image_path: Path to the input image
            - max_length: Maximum caption length (default: 50)
            - num_beams: Number of beams for generation (default: 4)
    
    Returns:
        Generated caption describing the image
    """
    from cv_tools import caption_image
    return await caption_image(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "caption_image",
            "description": "Generate a natural language caption describing the contents of an image using AI vision models.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "max_length": {
                        "type": "integer",
                        "description": "Maximum length of the generated caption in tokens. Default: 50",
                        "default": 50
                    },
                    "num_beams": {
                        "type": "integer",
                        "description": "Number of beams for beam search generation (higher = better quality but slower). Default: 4",
                        "default": 4
                    }
                },
                "required": ["image_path"]
            }
        }
    }
}
