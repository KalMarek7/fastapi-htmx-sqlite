from database import insert_image, get_images, get_image, update_image, insert_item, get_items, date_filtered_items, search_items, delete_item, get_item, update_item, clear_table
from models import User, Token, Items, ItemModel, UploadItem
from send import send_email
from typing import List
import base64
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Query, Security
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_403_FORBIDDEN
from sqlite3 import Connection, Row
from datetime import date, datetime
import os
import secrets

USERNAME = os.getenv("USERNAME", "not_set")
PASSWORD = os.getenv("PASSWORD", "not_set")
EMAIL = os.getenv("EMAIL", "not_set")

API_KEY_NAME = "X-API-Key"
API_KEY = secrets.token_urlsafe(32)
print(API_KEY)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def days_until_expiry(item: dict) -> int:
    return (item["expiry_date"] - date.today()).days


templates = Jinja2Templates(directory="templates")
templates.env.filters["days_until_expiry"] = days_until_expiry


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="You are missing API Key"
        )
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    return api_key_header


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
connection = Connection("./database/food.db")
connection.row_factory = Row


@ app.get("/restricted")
async def rest(request: Request, api_key: str = Depends(get_api_key)) -> HTMLResponse:
    # items = get_images(connection)
    return templates.TemplateResponse(request, "./index.html")


@ app.get("/")
async def root(request: Request) -> HTMLResponse:
    # items = get_images(connection)
    return templates.TemplateResponse(request, "./index.html")


@ app.get("/upload")
async def upload_site(request: Request) -> HTMLResponse:
    # items = get_images(connection)
    return templates.TemplateResponse(request, "./upload.html")


@ app.get("/api/v1/items")
async def fetch_items(request: Request, id: int = Query(None)) -> HTMLResponse:
    if not id:
        items = get_items(connection)
    else:
        items = get_item(connection, id)
    # print(items)
    return templates.TemplateResponse(request, "/items.html", context=items.model_dump())


@ app.get("/api/v1/images")
async def fetch_images(request: Request, id: int = Query(None)) -> HTMLResponse:
    """ images = get_images(connection)
    return templates.TemplateResponse(request, "./image.html", context=images.model_dump()) """
    if not id:
        images = get_images(connection)
    else:
        images = get_image(connection, id)
    # print(images.model_dump().keys())
    return templates.TemplateResponse(request, "/image.html", context=images.model_dump())


@ app.post("/api/v1/images")
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


@ app.get("/api/v1/edit_image/{id}")
async def start_edit(request: Request, id: int) -> HTMLResponse:
    # print(request.json)
    return templates.TemplateResponse(request, "./edit.html", context={"id": id})


@ app.put("/api/v1/edit_image/{id}")
async def edit_item(
        request: Request,
        id: int,
        name: str = Form(...),
        expiry_date: str = Form(...),
        picture_id: int = Form(...),
        category: str = Form(None),
        notes: str = Form(None)
) -> HTMLResponse:

    item = ItemModel(
        name=name,
        expiry_date=date.fromisoformat(expiry_date),
        created_date=datetime.now().date(),
        picture_id=id,
        category=category,
        notes=notes,
        item_id=id
    )
    # print("HAA", item)
    insert_item(connection, item)
    update_image(connection, id)
    return templates.TemplateResponse(request, "./modal.html", context={"id": id})


@ app.get("/api/v1/date_filtered_items")
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


@ app.post("/api/v1/search")
async def search(request: Request, search: str = Form(...)) -> HTMLResponse:
    # print(search)
    items = search_items(connection, search)
    if items.model_dump()["items"] == []:
        return HTMLResponse(content="<p>No items found</p>")
    return templates.TemplateResponse(request, "./items.html", context=items.model_dump())


@ app.delete("/api/v1/delete/{id}")
async def delete(request: Request, id: int) -> HTMLResponse:
    delete_item(connection, id)
    items = get_items(connection)
    return templates.TemplateResponse(request, "./items.html", context=items.model_dump())


@ app.get("/api/v1/item/{id}")
async def fetch_item(request: Request, id: int, action: str = Query(None)) -> HTMLResponse:
    if action == "edit":
        item = get_item(connection, id)
        return templates.TemplateResponse(request, "./edit_item.html", context=item.model_dump())
    else:
        item = get_item(connection, id)
        return templates.TemplateResponse(request, "./items.html", context=item.model_dump())


@ app.patch("/api/v1/item/{id}")
async def patch_item(
        id: int,
        request: Request,
        name: str = Form(...),
        expiry_date: str = Form(...),
        category: str = Form(None),
        notes: str = Form(None)
):
    update_item(connection, id=id, name=name, expiry_date=expiry_date,
                category=category, notes=notes)
    item = get_item(connection, id)
    return templates.TemplateResponse(request, "./items.html", context=item.model_dump())


@ app.get("/api/v1/clear/{table}")
async def cps(request: Request, table: str):
    clear_table(connection, table)
    return {"message": "success"}
