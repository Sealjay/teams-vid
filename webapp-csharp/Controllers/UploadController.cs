using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Hosting;
using TeamsVid.Config;
using Microsoft.Extensions.Options;
using Azure.Storage;
using Azure.Storage.Blobs;

namespace TeamsVid.Controllers
{
    [DisableRequestSizeLimit]
    public partial class UploadController : Controller
    {

        private readonly IOptions<AzureStorageConfig> _options;

        public UploadController(IOptions<AzureStorageConfig> options)
        {
            _options = options;
        }

        [HttpPost("upload/single")]
        public async Task<IActionResult> Single(IFormFile file)
        {
            //try
            //{
            Console.WriteLine($"Upload to blob storage starting.");
            if (file.Length > 0)
            {
                using (var stream = file.OpenReadStream())
                {
                    Uri blobUri = new Uri("https://" +
                                        _options.Value.AccountName +
                                        ".blob.core.windows.net/" +
                                        _options.Value.VideoContainer + "/" + file.FileName);

                    StorageSharedKeyCredential storageCredentials =
                        new StorageSharedKeyCredential(_options.Value.AccountName, _options.Value.AccountKey);

                    // Create the blob client.
                    BlobClient blobClient = new BlobClient(blobUri, storageCredentials);

                    // Upload the file
                    await blobClient.UploadAsync(stream, true);
                    Console.WriteLine($"URI: {blobUri}");
                }
            }

            Console.WriteLine($"{file.FileName} written to blob storage.");
            return StatusCode(200);
            //}
            //catch (Exception ex)
            //{
            //    Console.WriteLine(ex.Message);
            //    return StatusCode(500, ex.Message);
            //}
        }
    }
}