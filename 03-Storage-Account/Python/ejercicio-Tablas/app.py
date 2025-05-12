from flask import Flask, render_template, request, redirect, send_file
from azure.data.tables import TableServiceClient
import uuid

connection_str = "<connection string>"
table_name = "<table name>"
service = TableServiceClient.from_connection_string(connection_str)
table_client = service.get_table_client(table_name)
##table_client.create_table()

app = Flask(__name__)

@app.route("/")
def index():
    entities = table_client.query_entities(query_filter=None)
    return render_template("index.html", entities=entities)


@app.route("/save", methods=["POST"])
def save():
    tarea = request.form['tarea']
    prioridad = int(request.form['prioridad'])

    entity = {
        "PartitionKey": "",
        "RowKey": str(uuid.uuid4()),
        "Tarea": tarea,
        "Prioridad": prioridad
    }

    table_client.create_entity(entity=entity)
    return redirect("/")

@app.route("/delete/<row_key>")
def delete(row_key):
    table_client.delete_entity(partition_key="", row_key=row_key)
    return redirect("/")




app.run(debug=True)