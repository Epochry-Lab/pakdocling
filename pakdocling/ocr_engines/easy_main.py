import easyocr

file = "pakdocling/ocr_engines/input/bec.jpeg"

reader = easyocr.Reader(["ur", "en"], gpu=False)
result = reader.readtext(file)
print(result)
