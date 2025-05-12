using Azure;
using Azure.Data.Tables;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Company.Function
{
    public class GrabarTabla2
    {
        private readonly ILogger<GrabarTabla2> _logger;

        public GrabarTabla2(ILogger<GrabarTabla2> logger)
        {
            _logger = logger;
        }

        [Function("GrabarTabla2")]
        [TableOutput("personas", Connection = "AzureWebJobsStorage")]
        public ITableEntity Run([HttpTrigger(AuthorizationLevel.Anonymous, "get", "post")] HttpRequest req)
        {
            req.HttpContext.Response.StatusCode = 200;
            req.HttpContext.Response.WriteAsync($"Registrado: {req.Query["nombre"]} {req.Query["apellidos"]}");
            
            return new Persona() {
                Nombre = req.Query["nombre"],
                Apellidos = req.Query["apellidos"],
                PartitionKey = "demo",
                RowKey = Guid.NewGuid().ToString()
            };
        }
    }
}
