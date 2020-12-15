using System;
using System.IO;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;

namespace TeamsVid.Functions
{
    public static class UploadedVideo
    {
        [FunctionName("UploadedVideo")]
        public static void Run([BlobTrigger("videostoprocess/{name}", Connection = "AzureWebJobsStorage")] Stream newBlob, string name, ILogger log)
        {
            log.LogInformation($"Video upload processed blob\n Name:{name} \n Size: {newBlob.Length} Bytes",name);
        }
    }
}
