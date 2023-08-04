from PIL import Image
import io


def convert_image(image_file):
    pil_img = Image.open(image_file, mode='r')
    img_byte_arr = io.BytesIO()
    pil_img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
