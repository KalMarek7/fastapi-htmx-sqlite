from fastapi import FastAPI, File, UploadFile
from database import insert_image, get_images
from models import Items, ItemModel, UploadItem
from sqlite3 import Connection, Row
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from typing import List
import base64

app = FastAPI()
connection = Connection("./database/food.db")
connection.row_factory = Row

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request) -> HTMLResponse:
    # items = get_images(connection)
    return templates.TemplateResponse(request, "./index.html")


""" @app.get("/api/v1/items")
async def fetch_items(request: Request) -> HTMLResponse:
    items = get_items(connection)
    return templates.TemplateResponse(request, "./items.html", context=items.model_dump())


@app.post("/api/v1/item")
async def add_item(request: Request, item: ItemModel) -> HTMLResponse:
    print(item)
    print(await request.json())
    insert_item(connection, item)
    items = get_items(connection)
    return templates.TemplateResponse(request, "./items.html", context=items.model_dump()) """


@app.post("/api/v1/images")
async def upload(request: Request, file: List[UploadFile] = File(...)) -> HTMLResponse:
    for i in file:
        file_content = await i.read()
        print(i)
        encoded_data = base64.b64encode(file_content).decode("utf-8")
        filename = i.filename or "Default-name"
        filesize = i.size or 1337
        item = UploadItem(src=encoded_data,
                          filename=filename, filesize=filesize)
        insert_image(connection, item)

    images = get_images(connection)
    return templates.TemplateResponse(request, "./image.html", context=images.model_dump())


@app.get("/api/v1/images")
async def fetch_items(request: Request) -> HTMLResponse:
    images = get_images(connection)
    return templates.TemplateResponse(request, "./image.html", context=images.model_dump())


@app.get("/api/v1/edit_image/{id}")
async def start_edit(request: Request, id: int) -> HTMLResponse:
    print(request.json)
    return templates.TemplateResponse(request, "./edit.html", context={"id": id})


@app.post("/api/v1/edit_image/{id}")
async def edit(request: Request, id: int) -> HTMLResponse:
    print(request.json)
    return templates.TemplateResponse(request, "./edit.html", context={"id": id})
