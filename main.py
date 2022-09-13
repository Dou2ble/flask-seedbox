import hashlib
import os
from importlib.metadata import files
from pydoc import ispath
from zipfile import ZipFile

from flask import (Flask, after_this_request, current_app, redirect,
                   render_template, send_file, url_for)
from flask_cors import CORS

import utils


app = Flask(__name__)
CORS(app)


    


@app.route("/")
@app.route("/<path:path>")
def home(path=""):
    print()
    torrents = []
    full_path = "files\\" + path + "\\"
    for file in os.listdir(full_path):
        torrents.append({
            "type": utils.type(full_path + file),
            "name": file,
            "extension": utils.extension(full_path + file),
            "size": utils.sizeof_fmt(os.stat(full_path + file).st_size),
            "ratio" : 0.00
            })

    parent = "/".join(("/" + path).split("/")[0:-1])
    if parent == "":
        parent = "/"
        
    return render_template("index.html", torrents=torrents, path=path, parent=parent)
    

@app.route("/download/<path:path>", methods=["GET", "POST"])
def download(path):
    full_path = "files\\" + path
    return send_file(os.getcwd()+"\\" + full_path, as_attachment=True)

@app.route("/zip/<path:filename>", methods=["GET", "POST"])
def zip(filename):
    destination_file = "download.zip"
    
    with ZipFile("output\\" + destination_file, "w") as f:
        f.write("files\\" + filename)
        f.close()

    return send_file(os.getcwd() + "\\output\\" + destination_file, as_attachment=True)


@app.route("/md5/<path:path>", methods=["GET", "POST"])
def md5(path):
    full_path = "files\\" + path + "\\"
    destination_file = "checksum" + ".md5"
    hash = hashlib.md5(open("files\\" + path, "rb").read()).hexdigest()
    os.system(f'echo {hash} > "output\\{destination_file}"')

    return send_file(os.getcwd()+"\\output\\" + destination_file, as_attachment=True)


app.run(debug=True)
