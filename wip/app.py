from fastapi import FastAPI
from database import get_items, insert_item
from models import Items, ItemModel
from sqlite3 import Connection, Row
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

app = FastAPI()
connection = Connection("./database/food.db")
connection.row_factory = Row

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request) -> HTMLResponse:
    items = get_items(connection)
    return templates.TemplateResponse(request, "./index.html", context=items.model_dump())


@app.get("/api/v1/items")
async def fetch_items(request: Request) -> HTMLResponse:
    items = get_items(connection)
    return templates.TemplateResponse(request, "./items.html", context=items.model_dump())


@app.post("/api/v1/item")
async def add_pie(request: Request, pie: ItemModel) -> HTMLResponse:
    insert_item(connection, pie)
    items = get_items(connection)
    return templates.TemplateResponse(request, "./items.html", context=items.model_dump())
