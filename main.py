import base64
from PIL import Image
import re
from flask import Flask
from flask import render_template
from flask import request
import qrcode
import urllib.parse
import io
import htmlmin

app = Flask(__name__)


def url_encode_string(input_string):
    encoded_string = urllib.parse.quote(input_string)
    return encoded_string


@app.route("/create/html", methods=["GET", "POST"])
def qr_code_html():
    if request.method == "POST":
        data = request.form.get("file", "<h1 style='color:red'>Hello World!</h1>")
        data = htmlmin.minify(data, remove_empty_space=True,remove_comments=True,remove_all_empty_space=True,remove_optional_attribute_quotes=True,reduce_empty_attributes=True,reduce_boolean_attributes=True,keep_pre=True)
        code = data
        encoding = request.form.get("encodeSelect", "base64")
        data_url = ""
        if encoding == "base64":
            data_bytes = data.encode('utf-8')
            base64_bytes = base64.b64encode(data_bytes)
            data_url = "data:text/html;base64," + str(base64_bytes)[2:-1]
        elif encoding == "url":
            data_url = "data:text/html," + url_encode_string(data)
        elif encoding == "optimal":
            data_bytes = data.encode('utf-8')
            base64_bytes = base64.b64encode(data_bytes)
            data_url = "data:text/html;base64," + str(base64_bytes)[2:-1]
            if len("data:text/html," + url_encode_string(data)) < len(data_url):
                data_url = "data:text/html," + url_encode_string(data)
        img_data = ""
        try:
            qr_code_img = qrcode.make(data_url)
            qr_code_img.save('QRcode.png')
            with open("QRcode.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            img_data = "data:image/png;base64," + str(encoded_string)[2:-1]
        except ValueError:
            img_data = "error"
        return render_template("htmlqrready.html", url=data_url, img=img_data,
                               code=code, req="POST")
    if request.method == "GET":
        return render_template("htmlqrready.html", req="GET")


@app.route("/create/image", methods=["GET", "POST"])
def qr_code_img():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        pil_img = Image.open(uploaded_file, mode='r')
        img_byte_arr = io.BytesIO()
        pil_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        file_bytes=img_byte_arr
        encoded = base64.b64encode(file_bytes)
        img = "data:image/png;base64," + str(encoded)[2:-1]
        qr_data = ""
        try:
            qr_code_img = qrcode.make(img)
            qr_code_img.save('QRcode.png')
            with open("QRcode.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            qr_data = "data:image/png;base64," + str(encoded_string)[2:-1]
        except ValueError:
            qr_data = "error"
        return render_template("imgqrready.html", req="POST", url=img,img=qr_data)
    elif request.method == "GET":
        return render_template("imgqrready.html", req="GET")
