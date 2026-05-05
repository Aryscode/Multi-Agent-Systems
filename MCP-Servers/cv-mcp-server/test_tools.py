"""
Test script for CV MCP Server tools.

This script tests individual CV tools to ensure they work correctly.
"""

import asyncio
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)


async def test_detect_objects():
    """Test object detection tool."""
    from cv_tools import detect_objects
    
    logger.info("Testing object detection...")
    result = await detect_objects({
        "image_path": "test_image.jpg",
        "confidence_threshold": 0.5,
        "model_size": "n"
    })
    logger.info(f"Object detection result: {result}")
    return result


async def test_caption_image():
    """Test image captioning tool."""
    from cv_tools import caption_image
    
    logger.info("Testing image captioning...")
    result = await caption_image({
        "image_path": "test_image.jpg",
        "max_length": 50
    })
    logger.info(f"Captioning result: {result}")
    return result


async def test_classify_image():
    """Test image classification tool."""
    from cv_tools import classify_image
    
    logger.info("Testing image classification...")
    result = await classify_image({
        "image_path": "test_image.jpg",
        "top_k": 5,
        "model_name": "resnet50"
    })
    logger.info(f"Classification result: {result}")
    return result


async def main():
    """Run all tests."""
    logger.info("Starting CV MCP Server tests...")
    
    # You can uncomment these tests when you have test images
    # await test_detect_objects()
    # await test_caption_image()
    # await test_classify_image()
    
    logger.info("All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
