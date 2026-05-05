"""
Depth Estimation Tool

Estimates depth map from a single RGB image.
Returns relative depth information for scene understanding.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate depth from an image.
    
    Args:
        args: Dictionary containing:
            - image_path: Path to the input image
            - output_path: Path to save depth map (optional)
            - colorize: Whether to colorize the depth map (default: True)
    
    Returns:
        Depth estimation results and statistics
    """
    from cv_tools import depth_estimation
    return await depth_estimation(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "depth_estimation",
            "description": "Estimate depth map from a single RGB image. Returns relative depth information useful for 3D scene understanding.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional path to save the depth map visualization"
                    },
                    "colorize": {
                        "type": "boolean",
                        "description": "Whether to apply color mapping to the depth map for better visualization. Default: true",
                        "default": True
                    }
                },
                "required": ["image_path"]
            }
        }
    }
}
