from PIL import Image
from dotenv import load_dotenv
import pytesseract
import os

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("PYTESSERACT_INSTALLATION_PATH")

file = "pakdocling/ocr_engines/input/bec.jpeg"


print(pytesseract.get_languages(config=""))
print(pytesseract.image_to_string(Image.open(file), lang="urd"))
print(pytesseract.image_to_boxes(Image.open(file)))
print(pytesseract.image_to_data(Image.open(file)))
print(pytesseract.image_to_osd(Image.open(file)))
