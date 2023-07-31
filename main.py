import base64
import re
from flask import Flask
from flask import render_template
from flask import request
import qrcode
app = Flask(__name__)


def remove_special_characters(input_string):
    input_string = re.sub(' +', ' ', input_string)
    special_characters = ["\r", "\n", "\t"]
    for char in special_characters:
        input_string = input_string.replace(char, "")
    while '> <' in input_string:
        input_string = input_string.replace('> <', '><')
    return input_string


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/qrcode",methods=["GET", "POST"])
def qr_code():
    if request.method == "POST":
        data = request.form.get("file", "_")
        data = remove_special_characters(data)
        data_bytes = data.encode('ascii')
        base64_bytes = base64.b64encode(data_bytes)
        data_url = "data:text/html;base64,"+str(base64_bytes)[2:-1]
        qr_code = qrcode.make(data_url)
        qr_code.save('QRcode.png')
        with open("QRcode.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return render_template("QRcode.html",url = data_url,img = "data:image/png;base64,"+str(encoded_string)[2:-1])
    if request.method == "GET":
        return ":("