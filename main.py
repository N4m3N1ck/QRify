from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/qrcode",methods=["GET", "POST"])
def qr_code():
    if request.method == "POST":
        return request.form.get("file", "_")
    if request.method == "GET":
        return ":("