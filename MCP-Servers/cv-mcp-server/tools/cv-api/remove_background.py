"""
Background Removal Tool

Removes or replaces the background in images.
Useful for product photography and image editing.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove background from an image.
    
    Args:
        args: Dictionary containing:
            - image_path: Path to the input image
            - output_path: Path to save output image
            - background_color: Color for new background (default: transparent)
    
    Returns:
        Background removal results
    """
    from cv_tools import remove_background
    return await remove_background(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "remove_background",
            "description": "Remove or replace the background in an image. Outputs image with transparent or custom colored background.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path to save the output image with removed/replaced background"
                    },
                    "background_color": {
                        "type": "string",
                        "description": "Hex color code for new background (e.g., '#FFFFFF' for white) or 'transparent'. Default: 'transparent'",
                        "default": "transparent"
                    }
                },
                "required": ["image_path", "output_path"]
            }
        }
    }
}
