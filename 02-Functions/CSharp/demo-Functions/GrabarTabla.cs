using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Azure.Data.Tables;

namespace DemoFunctions
{
    public class GrabarTabla
    {
        private readonly ILogger<GrabarTabla> _logger;

        public GrabarTabla(ILogger<GrabarTabla> logger)
        {
            _logger = logger;
        }

        [Function("GrabarTabla")]
        public IActionResult Run([HttpTrigger(AuthorizationLevel.Anonymous, "get", "post")] HttpRequest req)
        {
            string nombre = req.Query["nombre"];
            string apellidos = req.Query["apellidos"];

            string storageConnection = Environment.GetEnvironmentVariable("AzureWebJobsStorage");
            if(!string.IsNullOrEmpty(storageConnection))
            {
                var client = new TableServiceClient(storageConnection);
                var table = client.GetTableClient("personas");

                var persona = new Persona() {
                    Nombre = nombre,
                    Apellidos = apellidos,
                    PartitionKey = "demo",
                    RowKey = Guid.NewGuid().ToString()
                };

                table.AddEntity(persona);
            }

            return new OkObjectResult($"Registrado: {nombre} {apellidos}");
        }
    }
}
