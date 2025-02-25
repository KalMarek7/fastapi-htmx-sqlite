from database import (
    insert_image,
    get_images,
    get_image,
    update_image,
    insert_item,
    get_items,
    date_filtered_items,
    search_items,
    delete_item,
    get_item,
    update_item,
    clear_table,
    delete_img,
    get_notification,
    switch_notification,
    insert_notification,
)
from models import User, Token, Items, ItemModel, UploadItem, Notification
from send import email_notification, start_scheduler, format_job
from typing import List
import base64
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Form,
    HTTPException,
    Depends,
    Query,
    Security,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from starlette.status import HTTP_403_FORBIDDEN
from sqlite3 import Connection, Row
from datetime import date, datetime
import os
import secrets
import magic
from apscheduler.schedulers.background import BackgroundScheduler

USERNAME = os.getenv("USERNAME", "not_set")
PASSWORD = os.getenv("PASSWORD", "not_set")
# EMAIL = os.getenv("EMAIL", "not_set")

API_KEY_NAME = "Authorization"
API_KEY = secrets.token_urlsafe(32)
print(API_KEY)
# print(datetime.now())
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
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key")
    return api_key_header


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Startup logic
        print("I AM NOW STARTING")
        notification = get_notification(connection).model_dump()
        print(notification)
        if notification["enabled"]:
            print("Found enabled notification at startup")
            email_dict = {
                "subject": f"{notification["subject"]}",
                "from_addr": f"{USERNAME}",
                "to_addr": f"{notification["to_addr"]}",
                "password": f"{PASSWORD}",
            }
            start_scheduler(
                scheduler, notification["days"], notification["time"], email_dict
            )
        else:
            print("No enabled notifications found")
        yield
    finally:
        # Shutdown logic
        print("I AM NOW STOPPING")
        # scheduler.remove_all_jobs()
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
connection = Connection("./database/food.db")
connection.row_factory = Row
scheduler = BackgroundScheduler()


@app.get("/restricted")
async def rest(request: Request, api_key: str = Depends(get_api_key)) -> HTMLResponse:
    # items = get_images(connection)
    return templates.TemplateResponse(request, "./index.html")


@app.get("/")
async def root(request: Request) -> HTMLResponse:
    # items = get_images(connection)
    return templates.TemplateResponse(request, "./index.html")


@app.get("/upload")
async def upload_site(request: Request) -> HTMLResponse:
    # items = get_images(connection)
    return templates.TemplateResponse(request, "./upload.html")


@app.get("/email")
async def email_site(request: Request) -> HTMLResponse:
    # print(scheduler.get_jobs()[0].next_run_time)
    notification = get_notification(connection).model_dump()
    if notification["enabled"]:
        notification["next_run_time"] = scheduler.get_jobs()[0].next_run_time
    print(notification)
    return templates.TemplateResponse(request, "./email.html", context=notification)


@app.patch("/email")
async def switch_email() -> HTMLResponse:
    notification = switch_notification(connection)
    enabled = notification.model_dump()["enabled"]
    print(f"Current email state: {enabled}")
    """ job_id = scheduler.get_jobs()[0].id
    print(job_id) """
    scheduler.shutdown()
    return HTMLResponse(
        content=f"""
        <span id='switch' class='text-red-500'>OFF</span>
        <button id='disable' class='hidden' hx-swap-oob='true'></button>
        <button
            id='submit'
            type='submit'
            class='w-full px-6 py-3 bg-[#2c4a3e] hover:bg-[#3d6b59] text-white font-semibold rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 mt-3'
            hx-swap-oob='true'
        >
            Submit
        </button>
        """
    )


@app.get("/api/v1/items")
async def fetch_items(request: Request, id: int = Query(None)) -> HTMLResponse:
    if not id:
        items = get_items(connection)
    else:
        items = get_item(connection, id)
    # print(items)
    return templates.TemplateResponse(
        request, "/items.html", context=items.model_dump()
    )


@app.get("/api/v1/images")
async def fetch_images(request: Request, id: int = Query(None)) -> HTMLResponse:
    """images = get_images(connection)
    return templates.TemplateResponse(request, "./image.html", context=images.model_dump())
    """
    if not id:
        images = get_images(connection)
    else:
        images = get_image(connection, id)
    # print(images.model_dump().keys())
    return templates.TemplateResponse(
        request, "/image.html", context=images.model_dump()
    )


@app.post("/api/v1/images")
async def upload(request: Request, file: List[UploadFile] = File(...)) -> HTMLResponse:
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    files_to_upload = []
    for i in file:
        file_content = await i.read()
        # print(i)
        mime_type = magic.from_buffer(file_content, mime=True)
        if mime_type not in allowed_types:
            print(f"Invalid file type {mime_type}")
            raise HTTPException(
                status_code=400,
                detail=f"""Invalid file type of {
                                mime_type}<br>Only jpeg, png, gif and webp are allowed""",
            )
        else:
            files_to_upload.append((i, file_content))

    for i, file_content in files_to_upload:
        encoded_data = base64.b64encode(file_content).decode("utf-8")
        filename = i.filename or "Default-name"
        filesize = i.size or 1337
        item = UploadItem(
            src=encoded_data, filename=filename, filesize=filesize, initial=True
        )
        insert_image(connection, item)

    images = get_images(connection)
    return templates.TemplateResponse(
        request, "./image.html", context=images.model_dump()
    )


@app.get("/api/v1/edit_image/{id}")
async def start_edit(request: Request, id: int) -> HTMLResponse:
    # print(request.json)
    return templates.TemplateResponse(request, "./edit.html", context={"id": id})


@app.put("/api/v1/edit_image/{id}")
async def edit_item(
    request: Request,
    id: int,
    name: str = Form(...),
    expiry_date: str = Form(...),
    picture_id: int = Form(...),
    category: str = Form(None),
    notes: str = Form(None),
) -> HTMLResponse:

    item = ItemModel(
        name=name,
        expiry_date=date.fromisoformat(expiry_date),
        created_date=datetime.now().date(),
        picture_id=id,
        category=category,
        notes=notes,
        item_id=id,
    )
    # print("HAA", item)
    insert_item(connection, item)
    update_image(connection, id)
    return templates.TemplateResponse(
        request, "./modal.html", context={"id": id, "name": name}
    )


@app.delete("/api/v1/delete_image/{id}")
async def delete_image(request: Request, id: int) -> HTMLResponse:
    image = get_image(connection, id)
    delete_img(connection, id)
    return templates.TemplateResponse(
        request, "./modal.html", context={"id": id, "name": image.images[0].filename}
    )


@app.post("/api/v1/date_filtered_items")
async def date_filtered_images(
    request: Request,
    email: str = Form(...),
    subject: str = Form(...),
    days=Form(...),
    time=Form(...),
) -> HTMLResponse:
    print(type(time), time)
    if len(time) > 5:
        return HTMLResponse(
            content=f"<p id='err' class='text-[#d4c3bc] mt-4'>'Time' field is invalid (too long)</p>"
        )
    try:
        days = int(days)
    except:
        return HTMLResponse(
            content=f"<p id='err' class='text-[#d4c3bc] mt-4'>'Days' field needs to be a number...</p>"
        )
    notification = Notification(
        enabled=True, subject=subject, to_addr=email, days=days, time=time
    )
    insert_notification(connection, notification)
    email_dict = {
        "subject": f"{subject}",
        "from_addr": f"{USERNAME}",
        "to_addr": f"{email}",
        "password": f"{PASSWORD}",
    }
    job = start_scheduler(scheduler, days, time, email_dict)
    return HTMLResponse(
        content=f"""
        <p id='err' class='text-[#d4c3bc] mt-4'>Job scheduled. Next run time at: <b>{job.next_run_time}</b></p>
        <span id='switch' hx-swap-oob='true' class='text-green-500'>ON</span>
        <button id='submit' hx-swap-oob='true' class='hidden'></button>
        <button
            id='disable'
            class='text-white bg-[#7a1a1a] hover:bg-[#951e1e] rounded-md px-4 py-2 mb-4 focus:outline-none focus:shadow-outline'
            hx-patch='/email'
            hx-trigger='click'
            hx-target='#switch'
            hx-swap='outerHTML'
            hx-swap-oob='true'
            onclick="removeReadOnly()"
        >
            Disable
        </button>
        """
    )


@app.post("/api/v1/search")
async def search(request: Request, search: str = Form(...)) -> HTMLResponse:
    # print(search)
    items = search_items(connection, search)
    if items.model_dump()["items"] == []:
        return HTMLResponse(content="<p>No items found</p>")
    return templates.TemplateResponse(
        request, "./items.html", context=items.model_dump()
    )


@app.delete("/api/v1/delete_item/{id}")
async def delete(request: Request, id: int) -> HTMLResponse:
    delete_item(connection, id)
    items = get_items(connection)
    return templates.TemplateResponse(
        request, "./items.html", context=items.model_dump()
    )


@app.get("/api/v1/item/{id}")
async def fetch_item(
    request: Request, id: int, action: str = Query(None)
) -> HTMLResponse:
    if action == "edit":
        item = get_item(connection, id)
        return templates.TemplateResponse(
            request, "./edit_item.html", context=item.model_dump()
        )
    else:
        item = get_item(connection, id)
        return templates.TemplateResponse(
            request, "./items.html", context=item.model_dump()
        )


@app.patch("/api/v1/item/{id}")
async def patch_item(
    id: int,
    request: Request,
    name: str = Form(...),
    expiry_date: str = Form(...),
    category: str = Form(None),
    notes: str = Form(None),
):
    update_item(
        connection,
        id=id,
        name=name,
        expiry_date=expiry_date,
        category=category,
        notes=notes,
    )
    item = get_item(connection, id)
    return templates.TemplateResponse(
        request, "./items.html", context=item.model_dump()
    )


@app.get("/api/v1/clear/{table}")
async def cps(request: Request, table: str):
    clear_table(connection, table)
    return {"message": "success"}


@app.get("/api/v1/schedule/")
async def get_schedule():
    scheduler.print_jobs()
    scheduled_jobs = scheduler.get_jobs()
    return {"schedule": [format_job(job) for job in scheduled_jobs]}
