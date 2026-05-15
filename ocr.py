"""Image OCR helpers used by the Streamlit app."""

import os
import tempfile
from pathlib import Path


try:
    from PIL import Image, ImageFilter, ImageOps

    PIL_AVAILABLE = True
except ImportError:
    Image = None
    ImageFilter = None
    ImageOps = None
    PIL_AVAILABLE = False

try:
    import easyocr

    OCR_AVAILABLE = True
    _reader = None
except ImportError:
    easyocr = None
    OCR_AVAILABLE = False
    _reader = None


def _get_reader():
    global _reader

    if not OCR_AVAILABLE:
        raise ImportError("EasyOCR is not installed. Run: pip install easyocr")

    if _reader is None:
        _reader = easyocr.Reader(["en"], gpu=False)
    return _reader


def extract_text_from_image(image_file, enhanced: bool = True) -> str:
    """Extract English text from a file path or a Streamlit uploaded file."""
    if isinstance(image_file, (str, Path)):
        return _do_ocr(str(image_file), enhanced=enhanced)

    suffix = Path(getattr(image_file, "name", "upload.png")).suffix or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(image_file.getvalue())
        tmp_path = tmp_file.name

    try:
        return _do_ocr(tmp_path, enhanced=enhanced)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def _do_ocr(image_path: str, enhanced: bool = True) -> str:
    reader = _get_reader()

    if not enhanced or not PIL_AVAILABLE:
        result = reader.readtext(image_path, detail=0, paragraph=True)
        return "\n".join(str(line).strip() for line in result if str(line).strip())

    candidates = _build_image_candidates(image_path)
    try:
        best_text = ""
        best_score = -1.0

        for candidate_path in candidates:
            text, score = _read_candidate(reader, candidate_path)
            if score > best_score:
                best_text = text
                best_score = score

        return best_text
    finally:
        for candidate_path in candidates[1:]:
            if os.path.exists(candidate_path):
                os.unlink(candidate_path)


def _read_candidate(reader, image_path: str) -> tuple[str, float]:
    result = reader.readtext(image_path, detail=1, paragraph=False)

    lines = []
    score = 0.0

    for item in result:
        if len(item) < 2:
            continue

        text = str(item[1]).strip()
        if not text:
            continue

        confidence = 0.5
        if len(item) >= 3:
            try:
                confidence = float(item[2])
            except (TypeError, ValueError):
                confidence = 0.5

        lines.append(text)
        score += max(confidence, 0.0) * max(len(text), 1)

    joined = "\n".join(lines)
    return joined, score


def _build_image_candidates(image_path: str) -> list[str]:
    original = str(image_path)
    candidates = [original]

    image = Image.open(image_path).convert("RGB")
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray)

    width, height = gray.size
    if max(width, height) < 1800:
        scale = min(3.0, 1800 / max(width, height))
        new_size = (int(width * scale), int(height * scale))
        gray = gray.resize(new_size, Image.Resampling.LANCZOS)

    sharp = gray.filter(ImageFilter.SHARPEN)
    candidates.append(_save_temp_image(sharp))

    high_contrast = ImageOps.autocontrast(sharp, cutoff=2)
    candidates.append(_save_temp_image(high_contrast))

    threshold = high_contrast.point(lambda pixel: 255 if pixel > 165 else 0)
    candidates.append(_save_temp_image(threshold))

    return candidates


def _save_temp_image(image) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        image.save(tmp_file.name)
        return tmp_file.name


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        print(extract_text_from_image(sys.argv[1]))
    else:
        print("Usage: python ocr.py <image_path>")
