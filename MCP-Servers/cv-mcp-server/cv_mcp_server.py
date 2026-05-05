"""
Computer Vision MCP Server

A Model Context Protocol server that provides computer vision tools including:
- Object detection
- Image segmentation
- Image captioning
- Image classification
- Feature extraction
- And more...
"""

import json
import logging
from typing import Any
import sys
import os
from pathlib import Path

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import Server
import mcp.server.stdio
from mcp.server.lowlevel import NotificationOptions
from mcp.shared.exceptions import McpError

from cv_tools import (
    detect_objects,
    segment_image,
    caption_image,
    classify_image,
    detect_faces,
    extract_features,
    pose_estimation,
    depth_estimation,
    style_transfer,
    remove_background,
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr,
    force=True
)
logger = logging.getLogger(__name__)

# Initialize MCP Server
server = Server("cv-mcp-server")

# Define Computer Vision Tools
TOOLS = [
    types.Tool(
        name="detect_objects",
        description="Detect objects in an image using YOLOv8. Returns bounding boxes, class labels, and confidence scores.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image file"
                },
                "confidence_threshold": {
                    "type": "number",
                    "description": "Minimum confidence score (0-1) for detections (default: 0.5)",
                    "default": 0.5
                },
                "model_size": {
                    "type": "string",
                    "description": "YOLO model size: 'n', 's', 'm', 'l', or 'x' (default: 'm')",
                    "enum": ["n", "s", "m", "l", "x"],
                    "default": "m"
                }
            },
            "required": ["image_path"]
        }
    ),
    types.Tool(
        name="segment_image",
        description="Perform semantic segmentation on an image. Returns segmented regions with labels.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image file"
                },
                "output_path": {
                    "type": "string",
                    "description": "Path to save the segmented image (optional)"
                },
                "model_type": {
                    "type": "string",
                    "description": "Segmentation model: 'sam', 'deeplabv3', or 'maskrcnn' (default: 'deeplabv3')",
                    "enum": ["sam", "deeplabv3", "maskrcnn"],
                    "default": "deeplabv3"
                }
            },
            "required": ["image_path"]
        }
    ),
    types.Tool(
        name="caption_image",
        description="Generate a natural language caption describing the contents of an image.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image file"
                },
                "max_length": {
                    "type": "integer",
                    "description": "Maximum length of the generated caption (default: 50)",
                    "default": 50
                },
                "num_beams": {
                    "type": "integer",
                    "description": "Number of beams for beam search (default: 4)",
                    "default": 4
                }
            },
            "required": ["image_path"]
        }
    ),
    types.Tool(
        name="classify_image",
        description="Classify an image into predefined categories using a pre-trained model.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image file"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of top predictions to return (default: 5)",
                    "default": 5
                },
                "model_name": {
                    "type": "string",
                    "description": "Model to use: 'resnet50', 'vit', or 'efficientnet' (default: 'resnet50')",
                    "enum": ["resnet50", "vit", "efficientnet"],
                    "default": "resnet50"
                }
            },
            "required": ["image_path"]
        }
    ),
    types.Tool(
        name="detect_faces",
        description="Detect faces in an image and return bounding boxes and facial landmarks.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image file"
                },
                "return_landmarks": {
                    "type": "boolean",
                    "description": "Whether to return facial landmarks (default: true)",
                    "default": True
                }
            },
            "required": ["image_path"]
        }
    ),
    types.Tool(
        name="extract_features",
        description="Extract deep feature vectors from an image using a pre-trained CNN.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image file"
                },
                "layer": {
                    "type": "string",
                    "description": "Layer to extract features from: 'pool', 'conv', or 'fc' (default: 'pool')",
                    "enum": ["pool", "conv", "fc"],
                    "default": "pool"
                }
            },
            "required": ["image_path"]
        }
    ),
    types.Tool(
        name="pose_estimation",
        description="Estimate human pose keypoints in an image.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image file"
                },
                "output_path": {
                    "type": "string",
                    "description": "Path to save the visualization (optional)"
                }
            },
            "required": ["image_path"]
        }
    ),
    types.Tool(
        name="depth_estimation",
        description="Estimate depth map from a single RGB image.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image file"
                },
                "output_path": {
                    "type": "string",
                    "description": "Path to save the depth map (optional)"
                },
                "colorize": {
                    "type": "boolean",
                    "description": "Whether to colorize the depth map (default: true)",
                    "default": True
                }
            },
            "required": ["image_path"]
        }
    ),
    types.Tool(
        name="style_transfer",
        description="Apply artistic style transfer to an image.",
        inputSchema={
            "type": "object",
            "properties": {
                "content_image": {
                    "type": "string",
                    "description": "Path to the content image"
                },
                "style_image": {
                    "type": "string",
                    "description": "Path to the style image"
                },
                "output_path": {
                    "type": "string",
                    "description": "Path to save the styled image"
                },
                "strength": {
                    "type": "number",
                    "description": "Style strength (0-1, default: 0.5)",
                    "default": 0.5
                }
            },
            "required": ["content_image", "style_image", "output_path"]
        }
    ),
    types.Tool(
        name="remove_background",
        description="Remove background from an image and optionally replace it.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image file"
                },
                "output_path": {
                    "type": "string",
                    "description": "Path to save the output image"
                },
                "background_color": {
                    "type": "string",
                    "description": "Hex color code for new background (default: transparent)",
                    "default": "transparent"
                }
            },
            "required": ["image_path", "output_path"]
        }
    ),
]

# Map tool names to functions
TOOL_FUNCTIONS = {
    "detect_objects": detect_objects,
    "segment_image": segment_image,
    "caption_image": caption_image,
    "classify_image": classify_image,
    "detect_faces": detect_faces,
    "extract_features": extract_features,
    "pose_estimation": pose_estimation,
    "depth_estimation": depth_estimation,
    "style_transfer": style_transfer,
    "remove_background": remove_background,
}


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available computer vision tools."""
    logger.info(f"Listing {len(TOOLS)} available tools")
    return TOOLS


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    logger.info(f"Tool called: {name}")
    logger.debug(f"Arguments: {arguments}")

    if name not in TOOL_FUNCTIONS:
        raise McpError(f"Unknown tool: {name}")

    if not arguments:
        raise McpError(f"Missing arguments for tool: {name}")

    try:
        # Execute the tool function
        result = await TOOL_FUNCTIONS[name](arguments)
        
        # Return the result as text content
        return [
            types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]
    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}", exc_info=True)
        raise McpError(f"Tool execution failed: {str(e)}")


async def main():
    """Run the CV MCP server."""
    logger.info("Starting CV MCP Server...")
    
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="cv-mcp-server",
            server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={},
            ),
        )
        await server.run(
            read_stream,
            write_stream,
            init_options
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
