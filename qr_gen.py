import qrcode
import io


def create_qr_code(data):
    qr_code_img_f = qrcode.make(data)
    qr_code_img_f = qr_code_img_f.convert("RGBA")
    datas = qr_code_img_f.getdata()
    newData = []
    for item in datas:
        if item[0] != 0 or item[1] != 0 or item[2] != 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    qr_code_img_f.putdata(newData)
    qr_bytes = io.BytesIO()
    qr_code_img_f.save(qr_bytes, format="PNG")
    return qr_bytes
