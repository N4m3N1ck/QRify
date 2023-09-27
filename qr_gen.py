# This software is licensed under the Creative Commons
# Attribution-NonCommercial 4.0 International License.
# To view a copy of this license, visit
# https://creativecommons.org/licenses/by-nc/4.0/
import qrcode
from PIL import Image
import io


def create_qr_code(data,fg_color,bg_color):
    qr = qrcode.QRCode(version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1)
    qr.add_data(data)
    qr.make(fit=True)
    qr_code_img_f = qr.make_image(fill_color=fg_color,back_color=bg_color)
    qr_code_img_f = qr_code_img_f.convert("RGBA")
    datas = qr_code_img_f.getdata()
    newData = []

    qr_code_img_f.putdata(newData)
    qr_bytes = io.BytesIO()
    qr_code_img_f.save(qr_bytes, format="PNG")
    return qr_bytes
