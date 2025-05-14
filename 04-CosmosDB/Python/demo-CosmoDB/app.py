from flask import Flask, render_template, request, redirect
from azure.cosmos import CosmosClient, PartitionKey
import os
import uuid

app = Flask(__name__)

COSMOS_URL = "<cosmos endpoint>"
COSMOS_KEY = "<cosmos key>"
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

@app.route("/editar/<id>/<categoria>", methods=["GET", "POST"])
def editar(id, categoria):
    if request.method == "GET":
        query = f"SELECT * FROM c WHERE c.id = '{id}'"
        items = list(container.query_items(query=query, partition_key=categoria))
        return render_template("editar.html", producto=items[0])
    else:
        nombre = request.form.get("nombre")
        categoria = request.form.get("categoria")
        precio = request.form.get("precio")
        stock = request.form.get("stock")

        producto = {
            "id": id,
            "nombre": nombre,
            "categoria": categoria,
            "precio": float(precio),
            "stock": int(stock)
        }

        container.replace_item(item=id, body=producto)

        return redirect("/")

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

@app.route("/", methods=["GET"])
def index():
    return render_template("listado.html", categorias=listado_categorias())

@app.route("/buscar", methods=["POST"])
def buscar():
    nombre = request.form.get("nombre")
    categoria = request.form.get("categoria")

    if(nombre == ""):
        query = "SELECT * FROM c"
    else:
        query = f"SELECT * FROM c WHERE CONTAINS(LOWER(c.nombre), LOWER('{nombre}'))"

    if(categoria == "all"):    
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
    else:
        items = list(container.query_items(query=query, partition_key=categoria))    

    return render_template("listado.html", productos=items, categorias=listado_categorias())

@app.route("/eliminar/<id>/<categoria>", methods=["GET"])
def eliminar(id, categoria):
    container.delete_item(item=id, partition_key=categoria)
    return redirect("/")

def listado_categorias():
    query = "SELECT DISTINCT c.categoria FROM c ORDER BY c.categoria"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    return items


app.run(debug=True)