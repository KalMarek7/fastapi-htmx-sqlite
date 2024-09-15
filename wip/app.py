from database import insert_image, get_images, update_image, insert_item, get_items, date_filtered_items, clear_table
from models import User, Token, Items, ItemModel, UploadItem
from send import send_email
from typing import List
import base64
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from sqlite3 import Connection, Row
from datetime import date
import os


app = FastAPI()

USERNAME = os.getenv("USERNAME", "not_set")
PASSWORD = os.getenv("PASSWORD", "not_set")
EMAIL = os.getenv("EMAIL", "not_set")

connection = Connection("./database/food.db")
connection.row_factory = Row

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request) -> HTMLResponse:
    # items = get_images(connection)
    return templates.TemplateResponse(request, "./index.html")


@app.get("/upload")
async def upload_site(request: Request) -> HTMLResponse:
    # items = get_images(connection)
    return templates.TemplateResponse(request, "./upload.html")


@app.get("/api/v1/items")
async def fetch_items(request: Request) -> HTMLResponse:
    items = get_items(connection)
    # print(items)
    return templates.TemplateResponse(request, "./items.html", context=items.model_dump())


""" @app.post("/api/v1/item")
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
                          filename=filename, filesize=filesize, initial=True)
        insert_image(connection, item)

    images = get_images(connection)
    return templates.TemplateResponse(request, "./image.html", context=images.model_dump())


@app.get("/api/v1/images")
async def fetch_images(request: Request) -> HTMLResponse:
    images = get_images(connection)
    return templates.TemplateResponse(request, "./image.html", context=images.model_dump())


@app.get("/api/v1/edit_image/{id}")
async def start_edit(request: Request, id: int) -> HTMLResponse:
    # print(request.json)
    return templates.TemplateResponse(request, "./edit.html", context={"id": id})


@app.post("/api/v1/edit_image/{id}")
async def edit_item(
        request: Request,
        id: int,
        name: str = Form(...),
        expiry_date: str = Form(...),
        picture_id: int = Form(...),
        category: str = Form(None),
        notes: str = Form(None)
) -> dict:

    item = ItemModel(
        name=name,
        expiry_date=date.fromisoformat(expiry_date),
        picture_id=id,
        category=category,
        notes=notes,
        item_id=id
    )
    # print("HAA", item)
    insert_item(connection, item)
    update_image(connection, id)
    return {"message": "success"}


@app.get("/api/v1/date_filtered_items")
async def date_filtered_images(request: Request):
    items = date_filtered_items(connection)
    items_dict = items.model_dump()
    if request.headers.get("custom_format") == "text/html":
        return templates.TemplateResponse(request, "./items.html", context=items.model_dump())
    else:
        message = ""
        for item in items_dict["items"]:
            message += f"""
            Name: {item['name']}<br>
            Expiry date: {item['expiry_date']}<br>
            Category: {item['category']}<br>
            Notes: {item['notes']}<br>
            <br><br>
            """

        message = "Hello. Below you'll find food items about to expire in the next 3 days.<br><br>" + message
        send_email(email={
            "subject": "Test Email from FastAPI",
            "message": message,
            "from_addr": f"{USERNAME}",
            "to_addr": f"{EMAIL}",
            "password": f"{PASSWORD}"
        })
        return {"message": "success"}


@app.get("/api/v1/clear/{table}")
async def cps(request: Request, table: str):
    clear_table(connection, table)
    return {"message": "success"}
