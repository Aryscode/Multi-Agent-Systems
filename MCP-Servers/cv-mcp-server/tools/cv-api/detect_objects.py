"""
Object Detection Tool

Detects objects in images using YOLOv8 model.
Returns bounding boxes, class labels, and confidence scores.
"""

import os
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


async def execute_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute object detection on an image.
    
    Args:
        args: Dictionary containing:
            - image_path: Path to the input image
            - confidence_threshold: Minimum confidence (default: 0.5)
            - model_size: YOLO model size (default: 'm')
    
    Returns:
        Detection results with bounding boxes and labels
    """
    from cv_tools import detect_objects
    return await detect_objects(args)


# Tool configuration
api_tool = {
    "function": execute_function,
    "definition": {
        "type": "function",
        "function": {
            "name": "detect_objects",
            "description": "Detect objects in an image using YOLOv8. Returns bounding boxes, class labels, and confidence scores for detected objects.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "confidence_threshold": {
                        "type": "number",
                        "description": "Minimum confidence score for detections (0-1). Default: 0.5",
                        "default": 0.5
                    },
                    "model_size": {
                        "type": "string",
                        "description": "YOLO model size: 'n' (nano), 's' (small), 'm' (medium), 'l' (large), or 'x' (extra large). Default: 'm'",
                        "enum": ["n", "s", "m", "l", "x"],
                        "default": "m"
                    }
                },
                "required": ["image_path"]
            }
        }
    }
}
