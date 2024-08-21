from fastapi import FastAPI
from database import get_pies, insert_pies
from models import Recipies, Recipie
from sqlite3 import Connection, Row
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

app = FastAPI()
connection = Connection("pie.db")
connection.row_factory = Row

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request) -> HTMLResponse:
    recipies = get_pies(connection)
    return templates.TemplateResponse(request, "./index.html", context=recipies.model_dump())


@app.get("/recipies")
async def get_recipies(request: Request) -> HTMLResponse:
    recipies = get_pies(connection)
    return templates.TemplateResponse(request, "./recipies.html", context=recipies.model_dump())


@app.post("/recipie")
async def add_pie(request: Request, pie: Recipie) -> HTMLResponse:
    insert_pies(connection, pie)
    recipies = get_pies(connection)
    return templates.TemplateResponse(request, "./recipies.html", context=recipies.model_dump())
