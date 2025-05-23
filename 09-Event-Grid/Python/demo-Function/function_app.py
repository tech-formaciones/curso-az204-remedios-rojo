import azure.functions as func
import logging, datetime, json, uuid, os
from azure.data.tables import TableServiceClient, TableEntity
from dotenv import load_dotenv


app = func.FunctionApp(http_auth_level=func.AuthLevel.ADMIN)

@app.route(route="httpEvent")
def httpEvent(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Iniciado el procesamiento del evento")

    load_dotenv()
    CONNECTION = os.getenv("AzureWebJobsStorage")
    TABLE_NAME = os.getenv("TableName", "Eventos")

    try:
        # Recuperar los datos del evento del cuerpo del mensaje
        data = json.loads(req.get_body())

        if not isinstance(data, list):
            data = [data]

        for event in data:
            if event.get("eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
                validation_code = event["data"]["validationCode"]
                logging.info(f"EventGrid validation code: {validation_code}")
                
                return func.HttpResponse(
                    json.dumps({"validationResponse": validation_code}),
                    status_code=200,
                    mimetype="application/json")

            id = event["data"].get("itemID", str(uuid.uuid4()))
            message = event["data"].get("message", "sin datos")

            # Grabar Datos
            service = TableServiceClient.from_connection_string(conn_str=CONNECTION)
            table = service.get_table_client(TABLE_NAME)

            registre = TableEntity()
            registre["PartitionKey"] = "Demos"
            registre["RowKey"] = id
            registre["Message"] = message
            registre["Fecha"] = datetime.datetime.utcnow().isoformat()

            table.create_entity(registre)

            # Finalizar la función retornando http response
            return func.HttpResponse(
                json.dumps({ "status": 200, "itemID": id}),
                status_code=200,
                mimetype="application/json")
    except Exception as e:
        logging.error(f"Error: {e}")

        return func.HttpResponse(
            json.dumps({ "error": str(e)}),
            status_code=400,
            mimetype="application/json")