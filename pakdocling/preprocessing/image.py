"""Image preprocessing utilities using OpenCV and NumPy for Pakistani document analysis."""

import os
from typing import Any, Union

import cv2
import numpy as np
from PIL import Image  # type: ignore[import-untyped]


class ImagePreprocessor:
    """Preprocesses document images for improved OCR text recognition accuracy."""

    @staticmethod
    def load_image(source: Union[str, bytes, np.ndarray, Image.Image]) -> np.ndarray:
        """Load image from path, bytes, PIL Image, or numpy array into OpenCV BGR array."""
        if isinstance(source, np.ndarray):
            if len(source.shape) == 2:
                return cv2.cvtColor(source, cv2.COLOR_GRAY2BGR)
            return source

        if isinstance(source, str):
            if not os.path.exists(source):
                raise FileNotFoundError(f"Image path does not exist: {source}")
            img = cv2.imread(source)
            if img is None:
                raise ValueError(f"Failed to decode image file: {source}")
            return img

        if isinstance(source, bytes):
            nparr = np.frombuffer(source, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Failed to decode image from bytes")
            return img

        if isinstance(source, Image.Image):
            rgb = np.array(source.convert("RGB"))
            return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        raise TypeError(f"Unsupported image source type: {type(source)}")

    @staticmethod
    def to_grayscale(img: np.ndarray) -> np.ndarray:
        """Convert BGR image to grayscale."""
        if len(img.shape) == 2:
            return img
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def enhance_contrast(
        gray_img: np.ndarray, clip_limit: float = 2.0, tile_grid_size: tuple[int, int] = (8, 8)
    ) -> np.ndarray:
        """Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)."""
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(gray_img)

    @staticmethod
    def denoise(gray_img: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """Denoise grayscale image using Gaussian blur."""
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.GaussianBlur(gray_img, (kernel_size, kernel_size), 0)

    @staticmethod
    def adaptive_threshold(gray_img: np.ndarray) -> np.ndarray:
        """Apply adaptive thresholding for binarization."""
        return cv2.adaptiveThreshold(
            gray_img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )

    @staticmethod
    def deskew(img: np.ndarray) -> np.ndarray:
        """Detect and correct document skew angle."""
        gray = ImagePreprocessor.to_grayscale(img) if len(img.shape) == 3 else img
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Find coordinates of all white pixels
        coords = np.column_stack(np.where(thresh > 0))
        if len(coords) < 10:
            return img

        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        # If angle is minor, don't over-correct
        if abs(angle) < 0.5 or abs(angle) > 45.0:
            return img

        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        m = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            img, m, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )
        return rotated

    def preprocess(
        self,
        source: Union[str, bytes, np.ndarray, Image.Image],
        do_deskew: bool = True,
        do_contrast: bool = True,
        do_denoise: bool = True,
        do_threshold: bool = False,
    ) -> dict[str, Any]:
        """Full image preprocessing pipeline.

        Returns dict containing processed grayscale image, processed color image, and metadata.
        """
        color_img = self.load_image(source)
        if do_deskew:
            color_img = self.deskew(color_img)

        gray = self.to_grayscale(color_img)

        if do_contrast:
            gray = self.enhance_contrast(gray)

        if do_denoise:
            gray = self.denoise(gray)

        final_img = self.adaptive_threshold(gray) if do_threshold else gray

        return {
            "color_image": color_img,
            "processed_gray": final_img,
            "width": color_img.shape[1],
            "height": color_img.shape[0],
            "channels": color_img.shape[2] if len(color_img.shape) == 3 else 1,
        }
