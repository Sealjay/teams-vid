from azure.storage import blob
import databases
import sqlalchemy
import uuid
from starlette.applications import Starlette
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import aiofiles
import multipart
from dotenv import dotenv_values
from azure.storage.blob.aio import BlobClient, BlobServiceClient
from azure.storage.blob import ContentSettings
import os

templates = Jinja2Templates(directory="templates")
config = dotenv_values(os.path.join(os.path.dirname(__file__), ".env"))


async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})


async def gallery(request):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{config['AZURE_STORAGE_ACCOUNT']}.blob.core.windows.net/",
        credential=config["AZURE_STORAGE_KEY"],
    )
    container_client = blob_service_client.get_container_client(
        config["AZURE_STORAGE_VIDEO_CONTAINER"]
    )
    blobs_list = []
    async for blob in container_client.list_blobs(include=["metadata"]):
        metadata = blob.metadata
        blobs_list.append(
            {
                "uuid": metadata["uuid"],
                "image_url": "https://bootsnipp.com/bootstrap-builder/libs/builder/icons/image.svg",
                "author": metadata["author"],
                "title": metadata["title"],
                "badge": metadata["badge"],
            }
        )
    await container_client.close()
    await blob_service_client.close()
    return templates.TemplateResponse(
        "gallery.html", {"request": request, "blobs": blobs_list}
    )


async def record(request):
    return templates.TemplateResponse("record.html", {"request": request})


async def play(request):
    return templates.TemplateResponse("play.html", {"request": request})


async def about(request):
    return templates.TemplateResponse("about.html", {"request": request})


async def add_file_to_db(file_name, file_contents, file_content_type):
    extension = file_name.split(".")[-1].lower()
    file_uuid_str = str(uuid.uuid4())
    new_filename = f"{file_uuid_str}.{extension}"
    async with aiofiles.open(f"uploads/{new_filename}", "wb") as file:
        await file.write(file_contents)
        await file.close()
    blob = BlobClient(
        account_url=f"https://{config['AZURE_STORAGE_ACCOUNT']}.blob.core.windows.net/",
        credential=config["AZURE_STORAGE_KEY"],
        container_name=config["AZURE_STORAGE_VIDEO_CONTAINER"],
        blob_name=new_filename,
    )

    await blob.upload_blob(
        file_contents,
        metadata={
            "original_file_name": file_name,
            "uuid": file_uuid_str,
            "author": "Dummy User",
            "title": "Dummy title",
            "badge": "dummy badge",
        },
        content_settings=ContentSettings(content_type=file_content_type),
    )
    await blob.close()


async def file_upload(request):
    form = await request.form()
    video_recording = form["video_recording"]
    filename = video_recording.filename
    content_type = video_recording.content_type
    contents = await video_recording.read()
    await add_file_to_db(filename, contents, content_type)
    return templates.TemplateResponse("uploaded.html", {"request": request})


routes = [
    Route("/", homepage),
    Route("/gallery", gallery),
    Route("/file_upload", file_upload, methods=["POST"]),
    Route("/record", record),
    Route("/play", play),
    Route("/about", about),
    Mount(
        "/static",
        app=StaticFiles(directory="static", packages=["bootstrap4"]),
        name="static",
    ),
]


app = Starlette(debug=True, routes=routes)
