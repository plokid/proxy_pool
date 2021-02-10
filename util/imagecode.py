from io import StringIO,BytesIO
from PIL import Image
import pytesseract

def image_to_code(content):

    image = Image.open(BytesIO(content))

    image = image.convert("L")

    code = pytesseract.image_to_string(image)                                                   

    return code.strip()