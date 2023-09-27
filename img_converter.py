# This software is licensed under the Creative Commons
# Attribution-NonCommercial 4.0 International License.
# To view a copy of this license, visit
# https://creativecommons.org/licenses/by-nc/4.0/
from PIL import Image
import io


def convert_image(image_file, img_format):
    pil_img = Image.open(image_file, mode='r')
    img_byte_arr = io.BytesIO()
    if img_format.upper()=="JPEG":
        pil_img = pil_img.convert("RGB")
    pil_img.save(img_byte_arr, format=img_format.upper())
    return img_byte_arr.getvalue()
