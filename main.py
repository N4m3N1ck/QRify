import base64
import re
from flask import Flask
from flask import render_template
from flask import request
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
        print(repr(data))
        data_bytes = data.encode('ascii')
        base64_bytes = base64.b64encode(data_bytes)
        return "data:text/html;base64,"+str(base64_bytes)[2:-1]
    if request.method == "GET":
        return ":("