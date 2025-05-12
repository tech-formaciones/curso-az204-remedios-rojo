using Azure;
using Azure.Data.Tables;

public class Persona : ITableEntity
{
    public string Nombre { get; set; }
    public string Apellidos { get; set; }
    public string PartitionKey { get; set; }
    public string RowKey { get; set; }
    public DateTimeOffset? Timestamp { get; set; }
    public ETag ETag { get; set; }

}