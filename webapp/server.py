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


templates = Jinja2Templates(directory="templates")


async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})


async def gallery(request):
    return templates.TemplateResponse("gallery.html", {"request": request})


async def record(request):
    return templates.TemplateResponse("record.html", {"request": request})


async def play(request):
    return templates.TemplateResponse("play.html", {"request": request})


async def about(request):
    return templates.TemplateResponse("about.html", {"request": request})


async def add_file_to_db(filename, file_contents):
    extension = filename.split(".")[-1].lower()
    file_uuid = uuid.uuid4()
    async with aiofiles.open(f"uploads/{file_uuid}.{extension}", "wb") as file:
        await file.write(file_contents)
        await file.close()


async def file_upload(request):

    form = await request.form()
    video_recording = form["video_recording"]
    filename = video_recording.filename
    contents = await video_recording.read()
    await add_file_to_db(filename, contents)
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
