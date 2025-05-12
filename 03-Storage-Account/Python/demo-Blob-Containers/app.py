from flask import Flask, render_template, request, redirect, send_file
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO

connection_str = "<connection string>"
container_name = "<container name>"
blob_client = BlobServiceClient.from_connection_string(connection_str)
container = blob_client.get_container_client(container_name)

app = Flask(__name__)

@app.route("/")
def index():
    blobs_var = container.list_blobs()
    return render_template("index.html", blobs=blobs_var)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
        blob_client = container.get_blob_client(file.filename)
        blob_client.upload_blob(file.read(), overwrite=True)

    return redirect("/")


@app.route("/descargar/<blob_name>")
def descargar(blob_name):
    blob_client = container.get_blob_client(blob_name)
    stream = blob_client.download_blob()

    return send_file(BytesIO(stream.readall()), as_attachment=True, download_name=blob_name)

@app.route("/eliminar/<blob_name>")
def eliminar(blob_name):
    blob_client = container.get_blob_client(blob_name)
    blob_client.delete_blob()

    return redirect("/")


@app.route("/ver/<blob_name>")
def ver_image(blob_name):
    return render_template("view_image.html", blob_name=blob_name)


app.run(debug=True)