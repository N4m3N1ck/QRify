from convert_to_b64 import *
from data_url_creator import *
from img_converter import *
from qr_gen import *
import re
from flask import Flask
from flask import render_template
from flask import request
import qrcode
import htmlmin

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
def qr_code_html():
    if request.method == "POST":
        data = request.form.get("file", "<h1 style='color:red'>Hello World!</h1>")
        data = htmlmin.minify(data, remove_empty_space=True, remove_comments=True, remove_all_empty_space=True,
                              remove_optional_attribute_quotes=True, reduce_empty_attributes=True,
                              reduce_boolean_attributes=True, keep_pre=True)
        data = remove_special_characters(data)
        code = data
        encoding = request.form.get("encodeSelect", "base64")
        data_url = ""
        if encoding == "base64":
            data_url = create_data_url("text", "html", True, string_to_b64(data), False)
        elif encoding == "url":
            data_url = create_data_url("text", "html", False, data, True)
        elif encoding == "optimal":
            data_url = create_data_url("text", "html", True, string_to_b64(data), False)
            if len(create_data_url("text", "html", False, data, True)) < len(data_url):
                data_url = create_data_url("text", "html", False, data, True)
        try:
            qr_code_img_f = qrcode.make(data_url)
            qr_bytes = io.BytesIO()
            qr_code_img_f.save(qr_bytes, format="PNG")
            encoded_string = base64.b64encode(qr_bytes.getvalue())
            img_data = create_data_url("image", "png", True, str(encoded_string)[2:-1], False)
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
        encoded = base64.b64encode(convert_image(uploaded_file))
        img = create_data_url("image", "png", True, str(encoded)[2:-1], False)
        try:
            qr_bytes = create_qr_code(img)
            encoded_string = base64.b64encode(qr_bytes.getvalue())
            qr_data = create_data_url("image", "png", True, str(encoded_string)[2:-1], False)
        except ValueError:
            qr_data = "error"
        if len(img) > 10 ** 6:
            display = False
        else:
            display = True
        return render_template("imgqrready.html", req="POST", url=img, img=qr_data, data_show=display)
    elif request.method == "GET":
        return render_template("imgqrready.html", req="GET")
