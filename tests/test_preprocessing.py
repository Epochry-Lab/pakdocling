"""Unit tests for OpenCV image preprocessing module."""

import numpy as np
from PIL import Image

from pakdocling.preprocessing import ImagePreprocessor


def test_load_image_numpy() -> None:
    arr = np.zeros((100, 100, 3), dtype=np.uint8)
    loaded = ImagePreprocessor.load_image(arr)
    assert loaded.shape == (100, 100, 3)


def test_load_image_pil() -> None:
    img = Image.new("RGB", (50, 50), color="white")
    loaded = ImagePreprocessor.load_image(img)
    assert loaded.shape == (50, 50, 3)


def test_grayscale_and_enhancement() -> None:
    preprocessor = ImagePreprocessor()
    arr = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

    gray = preprocessor.to_grayscale(arr)
    assert gray.shape == (100, 100)

    enhanced = preprocessor.enhance_contrast(gray)
    assert enhanced.shape == (100, 100)

    denoised = preprocessor.denoise(gray)
    assert denoised.shape == (100, 100)


def test_preprocess_pipeline() -> None:
    preprocessor = ImagePreprocessor()
    arr = np.ones((120, 120, 3), dtype=np.uint8) * 200

    result = preprocessor.preprocess(arr)
    assert "color_image" in result
    assert "processed_gray" in result
    assert result["width"] == 120
    assert result["height"] == 120
