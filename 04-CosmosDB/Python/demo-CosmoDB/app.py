from flask import Flask, render_template, request, redirect
from azure.cosmos import CosmosClient, PartitionKey
import os
import uuid

app = Flask(__name__)

COSMOS_URL = "https://demonosqlbcr.documents.azure.com:443/"
COSMOS_KEY = "GTUisV9jVwcGE4CLNJe3ZQRW3U15r9di8wnCLtNedD1jrQfOjl6Y22Wbyl6hSvWpg5ZhgHW1DbMyACDbTAOLCw=="
COSMOS_DB = "NorthwindDB"
COSMOS_CONTAINER = "Products"

# Crear cliente mediante cadena de conexión
#client = CosmosClient.from_connection_string("") 

# Crear cliente mediante URL y Clave
client = CosmosClient(COSMOS_URL, COSMOS_KEY)
database = client.create_database_if_not_exists(COSMOS_DB)
container = database.create_container_if_not_exists(
    id=COSMOS_CONTAINER,
    partition_key=PartitionKey("/categoria"))

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "GET":
        return render_template("registrar.html")
    else:
        nombre = request.form.get("nombre")
        categoria = request.form.get("categoria")
        precio = request.form.get("precio")
        stock = request.form.get("stock")

        producto = {
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "categoria": categoria,
            "precio": float(precio),
            "stock": int(stock)
        }

    container.upsert_item(producto)	

    return redirect("/")




app.run(debug=True)