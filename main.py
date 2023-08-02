import base64
import re
from flask import Flask
from flask import render_template
from flask import request
import qrcode
import urllib.parse

app = Flask(__name__)


def url_encode_string(input_string):
    encoded_string = urllib.parse.quote(input_string)
    return encoded_string


def remove_special_characters(input_string):
    input_string = re.sub(' +', ' ', input_string)
    special_characters = ["\r", "\n", "\t"]
    for char in special_characters:
        input_string = input_string.replace(char, "")
    return input_string


@app.route("/create/html", methods=["GET", "POST"])
def qr_code():
    if request.method == "POST":
        data = request.form.get("file", "<h1 style='color:red'>Hello World!</h1>")
        data = remove_special_characters(data)
        code = data
        encoding = request.form.get("encodeSelect", "base64")
        data_url = ""
        if encoding == "base64":
            data_bytes = data.encode('ascii')
            base64_bytes = base64.b64encode(data_bytes)
            data_url = "data:text/html;base64," + str(base64_bytes)[2:-1]
        elif encoding == "url":
            data_url = "data:text/html," + url_encode_string(data)
        elif encoding == "optimal":
            data_bytes = data.encode('ascii')
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
                               code=code,req="POST")
    if request.method == "GET":
        return render_template("htmlqrready.html",req="GET")
