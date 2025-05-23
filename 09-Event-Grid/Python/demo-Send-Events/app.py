from azure.eventgrid import EventGridPublisherClient, EventGridEvent
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import datetime, time, os, uuid


load_dotenv()
EVENTGRID_ENDPOINT = os.getenv("EVENTGRID_ENDPOINT")
EVENTGRID_KEY = os.getenv("EVENTGRID_KEY")

# Cliente para enviar eventos a un Event Grid Topic
client = EventGridPublisherClient(
    endpoint=EVENTGRID_ENDPOINT,
    credential=AzureKeyCredential(EVENTGRID_KEY))

for i in range(10):
    event = EventGridEvent(
        subject="Test -> Evento Generado",
        event_type="Demo.App.Test",
        data_version="1.0",
        data={
            "itemID": str(uuid.uuid4()),
            "message": f"Evento de prueba, generado {datetime.datetime.now()} [BORJA]"
        }
    )

    client.send([event])
    print(f"Evento {i + 1} enviado correctamente.")
    
    if i < 9:  # No dormir después del último evento
        time.sleep(20)