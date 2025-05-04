#
"""
AGIOTA SIMULATOR V0
"""
import os, re, asyncpg
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from libs import APP_GLOBALS
from rich import print
from contextlib import asynccontextmanager
from libs.databases.agdb_postgres.pool import create_pool
APP_GLOBALS = APP_GLOBALS()

    
@asynccontextmanager
async def _lifespan(app: FastAPI):
    # Code to run on startup
    print( "[bold black on white][AGIOTA SIMULATOR] - SETUP DE DIRETORIOS [/]\n" )
    for k in APP_GLOBALS.APP_DIRS.__dict__.keys():
        if not k.startswith("__") and not k.startswith("_"):
            os.makedirs(getattr(APP_GLOBALS.APP_DIRS, k), exist_ok=True)
        os.makedirs(os.path.join(APP_GLOBALS.APP_DIRS.MEDIA, "img"), exist_ok=True)
        os.makedirs(os.path.join(APP_GLOBALS.APP_DIRS.STATIC, "css"), exist_ok=True)
        os.makedirs(os.path.join(APP_GLOBALS.APP_DIRS.STATIC, "js"), exist_ok=True)
        os.makedirs(os.path.join(APP_GLOBALS.APP_DIRS.MIDDLEWARE, "auth"), exist_ok=True)
    print( "[bold black on white][AGIOTA SIMULATOR] - SETUP DE DIRETORIOS - OK [/]" )
    print( "[bold black on white][AGIOTA SIMULATOR] - SETUP DE DATABASE[/]" )
    app.state.GAME_START_DATE = datetime.strptime('2025-01-01 00:00:00 -0300', '%Y-%m-%d %H:%M:%S %z')
    app.state.agdb_pool = await create_pool()
    yield

    # Code to run on shutdown
    print("[bold black on white][AGIOTA SIMULATOR] - EXECUTANDO SHUTDOWN[/]")
    # Clean up resources
    print("[bold black on white][AGIOTA SIMULATOR] - SHUTDOWN COMPLETO[/]")


app = FastAPI(lifespan=_lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """
    Middleware to handle authentication and authorization
    """
    public_routes = [r"^/$", r"^/static/.*", r"^/media/.*",  r"^/login$", r"^/test$",r"^/new-office$",r"^/enter-office$", r"^/my-office$"]
    if any(re.match(pattern, request.url.path) for pattern in public_routes):
        return await call_next(request) #mandou pro endpoint

    #print(f"[bold black on white][AGIOTA SIMULATOR] - ROTA PRIVADA - {request.url.path} [/]")
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        redirect_response = RedirectResponse(url="/login")
        redirect_response.set_cookie(key="forward_login", value=request.url.path, httponly=True)        
        return redirect_response

    response = await call_next(request)
    return response
    

templates = Jinja2Templates(directory=APP_GLOBALS.APP_DIRS.TEMPLATES)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/")
async def index(request: Request):
   return  templates.TemplateResponse("home.html", {"request": request, "title": APP_GLOBALS.APP_NAME, "version": APP_GLOBALS.APP_VERSION, "description": APP_GLOBALS.APP_DESCRIPTION})

from routes.login import login_router
app.include_router(login_router, tags=["login"], include_in_schema=False)

#

