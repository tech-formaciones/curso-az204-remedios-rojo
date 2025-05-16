import requests
import json
from msal import ConfidentialClientApplication

import os
os.system("cls" if os.name == "nt" else "clear")

# Generar la aplicación o cliente

client = ConfidentialClientApplication(
    client_id="<client id>",
    client_credential="<secret>",
    authority="https://login.microsoftonline.com/<tenant id>")


 # Generar el Token
scopes = ["https://graph.microsoft.com/.default"]
result = client.acquire_token_for_client(scopes=scopes)

if "access_token" in result:
    print(result["access_token"])
else:
    print("Error al obtener el token")
    print(result.get("error"))
    print(result.get("error_description"))
    exit()

input("Pulsa una tecla para continuar")
os.system("cls" if os.name == "nt" else "clear")

# Listado de usuarios mediante HTTP

url = "https://graph.microsoft.com/v1.0/users"
headers = { "Authorization" : f"Bearer {result["access_token"]}"}
response = requests.get(url, 0)

if response.status_code == 200:
    data = response.json()
    users = data.get("value", [])
    for user in users:
        print(f" -> {user.get("displayName")} - {user.get("userPrincipalName")}")
else:
    print(f"Error {response.status_code}: {response.text}")