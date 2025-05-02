from fastapi import Request, Form, Depends
from fastapi.responses import Response, RedirectResponse, HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from agiota import APP_GLOBALS, templates, get_agdb_pool
from libs.agdb.repos.players import AgdbPlayerRepository

login_routes = APIRouter()

@login_routes.get("/login", include_in_schema=False)
async def login_page(request: Request, agdb_pool=Depends(get_agdb_pool)):
    """
    Login page
    """
    cookies = request.cookies
    return templates.TemplateResponse("login.html", {"request": request})

@login_routes.post("/enter-office")
async def try_auth(request: Request, username: str = Form(...), password: str = Form(...), agdb_pool=Depends(get_agdb_pool)):
    """
    Autentica um agiota
    Auths a loanshark
    """
    #testa o agdb_pool
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@login_routes.post("/new-office")
async def create_user(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """
    Cria um agiota
    Creates a loanshark
    """
    if name and email and password:
        await AgdbPlayerRepository.create_player_with_password(name, email, password)
        return JSONResponse(content={"message": "User created successfully"}, status_code=201)
    else:
        return JSONResponse(content={"error": "Invalid data"}, status_code=400)


@login_routes.get("/test")
async def test(request: Request, agdb_pool=Depends(get_agdb_pool)):
    """
    Teste de rota
    Test route
    """
    async with agdb_pool.acquire() as connection:
        async with connection.transaction():
            result = await connection.fetch("SELECT 1")
            return JSONResponse(content={"result": [dict(record) for record in result]}, status_code=200)
    
    return templates.TemplateResponse("game/boilerplate.html", {"request": request, "title": APP_GLOBALS.APP_NAME, "version": APP_GLOBALS.APP_VERSION, "description": APP_GLOBALS.APP_DESCRIPTION})