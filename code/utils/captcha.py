import cairosvg
import time
import re
from PIL import Image
import os
import pytesseract


def bypass_captcha(svg: str) -> str:
    """_summary_
    Read captcha code by pytesseract
    Args:
        svg (str): svg text from api

    Returns:
        str: captcha code with svg text from api
    """
    file_name = str(int(time.time() * 1000)) + ".svg"
    regex = r"<path[^>]*stroke=[^>]*>"
    new_svg = re.sub(regex, '', svg)
    f = open(file_name, "w")
    f.write(new_svg)
    f.close()
    cairosvg.svg2png(url=file_name, write_to="output.png")
    image = Image.open("output.png")

    text: str = pytesseract.image_to_string(
        image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    # Remove file after used
    os.remove(file_name)
    os.remove("output.png")

    return text.strip()
