import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:/Tesseract-OCR/tesseract'

img = Image.open("capture.jpg")

print(pytesseract.image_to_string(img, lang='eng'))
