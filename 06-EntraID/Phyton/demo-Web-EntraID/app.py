from flask import Flask, session, url_for, render_template, request, redirect, send_file
from msal import ConfidentialClientApplication
import os
import uuid

from functools import wraps

CLIENT_ID="<client id>"
CLIENT_SECRET="<client secret>"
AUTHORITY="https://login.microsoftonline.com/<tenant id>"
REDIRECT_URL="http://localhost:5000/getAToken"
SCOPE = ["User.Read"]

app = Flask(__name__)
app.secret_key = os.urandom(32)

############################################################

# Inicializar MSAL, creando el cliente
def _build_msal_app(cache=None):
    return ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
        token_cache=cache)

# Contruir la URL de inicio de sesión
def _build_auth_url():
    return _build_msal_app().get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=REDIRECT_URL,
        state=str(uuid.uuid4()))

# Obtener el Token desde el código autorización
def _get_token_from_code(auth_code):
    result = _build_msal_app().acquire_token_by_authorization_code(
        auth_code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URL)
    
    return result
    
# Decorador para proteger las rutas de la Web
def login_required(f):
    @wraps(f)
    def decorate_function(*args, **kwargs):
        if "user" not in session:
           return redirect(url_for("login"))
        return f(*args, **kwargs)
    
    return decorate_function

############################################################

@app.route("/login")
def login():
    return redirect(_build_auth_url())

@app.route("/logout")
def logout():
    session.clear()
    return redirect("https://login.microsoftonline.com/common/oauth2/v2.0/logout"
                    f"?post_logout_redirect_uri={url_for("index", _external=True)}")

@app.route("/getAToken")
def getAToken():
    result = _get_token_from_code(request.args["code"])
    if "access_token" in result:
        session["user"] = result.get("id_token_claims")
    return redirect(url_for("index"))

############################################################

@app.route("/")
def index():
    return render_template("index.html", user=session.get("user"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=session["user"])

@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html", user=session["user"])


app.run(debug=True)