"""
Pose Estimation Tool

Estimates human pose keypoints in images.
Returns skeletal keypoints for body joints.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate human pose in an image.
    
    Args:
        args: Dictionary containing:
            - image_path: Path to the input image
            - output_path: Path to save visualization (optional)
    
    Returns:
        Pose keypoints for detected people
    """
    from cv_tools import pose_estimation
    return await pose_estimation(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "pose_estimation",
            "description": "Estimate human pose keypoints in an image. Returns skeletal keypoints for body joints (shoulders, elbows, knees, etc.).",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional path to save a visualization of the detected pose"
                    }
                },
                "required": ["image_path"]
            }
        }
    }
}
