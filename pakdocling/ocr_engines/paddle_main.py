from paddleocr import PaddleOCR

# Uses PP-OCRv6 models by default
ocr = PaddleOCR(
    use_doc_orientation_classify=False,  # Disables document orientation classification model via this parameter
    use_doc_unwarping=False,  # Disables text image rectification model via this parameter
    use_textline_orientation=False,  # Disables text line orientation classification model via this parameter
    lang="ur",
)

file = "pakdocling/ocr_engines/input/bec.jpeg"
result = ocr.predict(file)
for res in result:
    res.print()
