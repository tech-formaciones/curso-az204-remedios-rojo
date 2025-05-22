from flask import Flask, request, url_for, render_template, redirect
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential, ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import HttpResponseError

app = Flask(__name__)

KEY_VAULT_URL = "<key vault url>"

# Solicitar credenciales mediante el navegador
credential = InteractiveBrowserCredential(additionally_allowed_tenants=["*"])


# Solicitar credenciales mediantes varios mecanimos de autenticación:
# - definidas medinate variables de entorno:
#    - AZURE_CLIENT_ID
#    - AZURE_CLIENT_SECRET
#    - AZURE_TENANT_ID
# - registros de autenticación en la cache
# - registros de usuarios (credenciales del equipo)

# credential = DefaultAzureCredential()


# Solicitar credenciales mediante un principal de Servicio (usuario de las App)

# credential = ClientSecretCredential(
#     tenant_id="",
#     client_id="",
#     client_secret="")

client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

@app.route("/")
def index():
    try:
        secrets = list(client.list_properties_of_secrets())
        return render_template("index.html", secrets=secrets)
    except HttpResponseError as e:
        if e.status_code == 403:
            error_msg = "No autorizado: el usuario no tiene permiso para acceder a los secretos de Key Vault."            
        else:
            error_msg = e.error
        
        return render_template("index.html", secrets=[], error=error_msg)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    secret = request.form["secret"]

    client.set_secret(name, secret)

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form["name"]
    transaction = client.begin_delete_secret(name)
    transaction.wait()
    return redirect("/")

@app.route("/view/<name>")
def view(name):
    try:
        secret = client.get_secret(name)
        secrets = list(client.list_properties_of_secrets())

        return render_template("index.html", 
                               secrets=secrets,
                               message=f"Secreto {name}: {secret.value}")
    except HttpResponseError as e:
        if e.status_code == 403:
            error_msg = "No autorizado: el usuario no tiene permiso para acceder a los secretos de Key Vault."            
        else:
            error_msg = e.error
        
        return render_template("index.html", secrets=[], error=error_msg)




app.run(debug=True)