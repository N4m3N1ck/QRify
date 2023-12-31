# This software is licensed under the Creative Commons
# Attribution-NonCommercial 4.0 International License.
# To view a copy of this license, visit
# https://creativecommons.org/licenses/by-nc/4.0/
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

@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/create/html")
def qr_code_html():
    return render_template("htmlqrready.html")


@app.route("/create/image", methods=["GET", "POST"])
def qr_code_img():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        img_format = request.form.get("formatSelect","PNG")
        encoded = base64.b64encode(convert_image(uploaded_file,img_format))
        img = create_data_url("image", img_format.lower(), True, str(encoded)[2:-1], False)
        try:
            qr_bytes = create_qr_code(img, "black", "white")
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
@app.route("/post",methods=["POST"])
def qr_ready():
    if request.method == "POST":
        data = request.form.get("file", "<h1 style='color:red'>Hello World!</h1>")
        fg_color = request.form.get("frontColor")
        bg_color = request.form.get("backColor")
        minimize = request.form.get("min")!=None
        if minimize:
            data = htmlmin.minify(data, remove_empty_space=True, remove_comments=True, remove_all_empty_space=True,
                              remove_optional_attribute_quotes=True, reduce_empty_attributes=True,
                              reduce_boolean_attributes=True, keep_pre=True)
        if minimize:
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
            qr_bytes = create_qr_code(data_url,fg_color, bg_color)
            encoded_string = base64.b64encode(qr_bytes.getvalue())
            img_data = create_data_url("image", "png", True, str(encoded_string)[2:-1], False)
        except ValueError:
            img_data = "error"
        return render_template("post.html", url=data_url, img=img_data,
                               code=code, req="POST")
        
