# main.py
import os
from fastapi import FastAPI, Request, Form
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.database import *
from backend.app.api import product, fridge, task, reminder
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# Инициализация базы данных
@app.on_event("startup")
async def startup_db_client():
    print("startup db client")

@app.on_event("shutdown")
async def shutdown_db_client():
    await mongodb.close()

# Подключение маршрутов из отдельных модулей
app.include_router(product.router, prefix="/api/products", tags=["Products"])
app.include_router(fridge.router, prefix="/api/fridge", tags=["Fridge"])
app.include_router(task.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(reminder.router, prefix="/api/reminder", tags=["Reminder"])

@app.get("/")
async def index(request: Request):
    login = request.cookies.get("login")
    return templates.TemplateResponse("index.html", {"request": request, "login": login})

@app.get("/fridge")
async def fridge(request: Request):
    return templates.TemplateResponse("fridge.html", {"request": request})

@app.post("/login")
async def login(request: Request, login: str = Form(...)):
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="login", value=login)
    return response