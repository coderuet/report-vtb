import time
from cachetools.func import lru_cache
from cachetools import TTLCache
import xml.etree.ElementTree as ET
import pytesseract
from PIL import Image
import cairosvg

# svg_file = "1747182183167.svg"
# png_file = "output.png"
# cairosvg.svg2png(url=svg_file, write_to=png_file, scale=2.0)


# image = Image.open("output.png")

# text = pytesseract.image_to_string(
#     image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
# print("xxxx", text.strip())

# tree = ET.parse("1747093721763.svg")
# root = tree.getroot()
# print("xxx", root)
# # element_to_remove = root.findall(".//path")
# # print("xxx", element_to_remove)
# # Example: Remove elements with specific text content
# targets = ["stroke="]
# for element in root.iter("*"):
#     print("xxx", element.text)
#     if (element.text is not None) and any(item in element.text for item in targets):
#         print("xxx")
#         root.remove(element)
# tree.write("modified_svg_file.svg")


# Create a TTL cache with max size 100 and TTL of 10 seconds
from cachetools import TTLCache
from cachetools import cached
import time
from collections import defaultdict
from datetime import datetime
# Create a TTL cache with max size 100 and TTL of 10 seconds
cache = TTLCache(maxsize=100, ttl=10)

# Use the cached decorator from cachetools (not functools.lru_cache)

formatted_date = datetime.strptime(
    "2025-04-30", "%Y-%m-%d").strftime("%Y-%m-%d")
print("xxx", formatted_date)
print("xx", str(formatted_date)[:-3])
