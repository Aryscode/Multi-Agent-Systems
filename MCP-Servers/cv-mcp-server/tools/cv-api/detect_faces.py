"""
Face Detection Tool

Detects faces in images and returns bounding boxes.
Optionally returns facial landmarks.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect faces in an image.
    
    Args:
        args: Dictionary containing:
            - image_path: Path to the input image
            - return_landmarks: Whether to return facial landmarks (default: True)
    
    Returns:
        Face detection results with bounding boxes and optional landmarks
    """
    from cv_tools import detect_faces
    return await detect_faces(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "detect_faces",
            "description": "Detect faces in an image and return bounding boxes. Optionally returns facial landmarks for detected faces.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "return_landmarks": {
                        "type": "boolean",
                        "description": "Whether to return facial landmark points (eyes, nose, mouth, etc.). Default: true",
                        "default": True
                    }
                },
                "required": ["image_path"]
            }
        }
    }
}
