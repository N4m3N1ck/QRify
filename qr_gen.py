import qrcode
import io


def create_qr_code(data):
    qr_code_img_f = qrcode.make(data)
    qr_bytes = io.BytesIO()
    qr_code_img_f.save(qr_bytes, format="PNG")
    return qr_bytes
