from fastapi import Request, Form, Depends
from fastapi.responses import Response, RedirectResponse, HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from agiota import APP_GLOBALS, templates, app
from rich import print
from libs.spb_auth.supabase_auth import supabase, verify_jwt
from models import PlayerModels, SessionModels
from libs.databases.agdb_postgres.repos import PlayersRepo

ROUTER_TRACE = True
ROUTER_DEBUG = True

login_router = APIRouter()

@login_router.post("/enter-office")
async def enter_office(request: Request, email: str = Form(...), password: str = Form(...)):
    """
    Autentica um agiota
    """
    #loga no supabase
    try:
        login = supabase.auth.sign_in_with_password({'email':email, 'password':password})
    except Exception as e:
        print("[bold red]Error logging in:", e)
        return JSONResponse(status_code=400, content={"error": "Error logging in"})
    
    session = {'at': login.session.access_token, 'rt': login.session.refresh_token}
    try:
        player = await PlayersRepo.Fetch.player_by_id(app.state.agdb_pool, login.user.id)
    except Exception as e:
        print("[bold red]Error fetching player:", e)
        return JSONResponse(status_code=400, content={"error": "Error fetching player"})
    
    _response = RedirectResponse(url="/my-office", status_code=303)
    _response.set_cookie(key="agsm-at", value=session['at'], httponly=True)
    _response.set_cookie(key="agsm-rt", value=session['rt'], httponly=True)
    return _response

@login_router.post("/new-office")
async def new_office(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """
    Cria um agiota
    """
    #cria no supabase
    try:
        signup = supabase.auth.sign_up({'email':email, 'password':password})
    except Exception as e:
        print("[bold red]Error creating user:", e)
        return JSONResponse(status_code=400, content={"error": "Error creating user"})
    
    session = {'at': signup.session.access_token, 'rt': signup.session.refresh_token}
    new_player = PlayerModels.NewPlayer(
        id=signup.user.id,
        name=name,
        email=email
    )    

    try:
        await PlayersRepo.Insert.new_player(app.state.agdb_pool , new_player)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Error creating user in database {e}"})

    #cria os cookies
    _response = RedirectResponse(url="/my-office", status_code=303)
    _response.set_cookie(key="agsm-at", value=session['at'], httponly=True)
    _response.set_cookie(key="agsm-rt", value=session['rt'], httponly=True)
    return _response

@login_router.get("/logout")
async def logout(request: Request):
    """
    Logout do agiota
    """
    _response = RedirectResponse(url="/", status_code=303)
    _response.delete_cookie(key="agsm-at")
    _response.delete_cookie(key="agsm-rt")
    return _response

@login_router.get("/my-office")
async def my_office_page(request: Request):
    _at, _rt = request.cookies.get("agsm-at"), request.cookies.get("agsm-rt")
    if not _at or not _rt:
        return RedirectResponse(url="/", status_code=303)
    
    session_info = verify_jwt(_at)
    session_info = SessionModels.Session(
        iss=session_info['iss'],
        sub=session_info['sub'],
        session_id=session_info['session_id'],
        refresh_token=_rt,
        exp=session_info['exp'],
        iat=session_info['iat']
    )
    player = await PlayersRepo.Fetch.player_by_id(app.state.agdb_pool, session_info.sub)    
    print(player)
    return templates.TemplateResponse("game/boilerplate.html", {"request": request, "title": APP_GLOBALS.APP_NAME, "version": APP_GLOBALS.APP_VERSION, "description": APP_GLOBALS.APP_DESCRIPTION, "player": player.model_dump_json()})