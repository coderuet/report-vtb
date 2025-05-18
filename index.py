import xml.etree.ElementTree as ET
import pytesseract
from PIL import Image
import cairosvg

svg_file = "1747182183167.svg"
png_file = "output.png"
cairosvg.svg2png(url=svg_file, write_to=png_file, scale=2.0)


image = Image.open("output.png")

text = pytesseract.image_to_string(
    image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
print("xxxx", text.strip())

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
