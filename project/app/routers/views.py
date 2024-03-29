import starlette.status
import sqlalchemy.orm
import fastapi
import os

from fastapi import APIRouter
from fastapi import templating
from fastapi import Depends, Request, Response, Header
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.internal.jwt import JWTBearer
from app.utils import TEMPLATE_DIRECTORY_PATH, log, STORAGE_DIRECTORY_PATH, session as Session
from app.maintainer import get_token, validate_token_ as validate_token
from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer()
router = APIRouter()

template = templating.Jinja2Templates(
    directory=TEMPLATE_DIRECTORY_PATH
)


async def session():
    database = Session()
    try:
        yield database

    except Exception as exception:
        log.exception(exception)

    finally:
        database.close()


'''
@router.get("/")
async def root(request: Request) -> HTMLResponse:
    token: str = fastapi.Header(None, alias="Authorization")
    if token is None:
        return template.TemplateResponse("sign-in.html", {"request": request})
    
    decoded_token = validate_token(token=token, output=True)

    if decoded_token:
        return template.TemplateResponse("application.html", {"request": request})
    else:
        return template.TemplateResponse("sign-in.html", {"request": request})
'''


@router.get(path="/")
async def root(request: Request):
    print(f'{request.cookies=}')
    print(f'{request.headers=}')
    
    try:
        return template.TemplateResponse("sign-in.html", {"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}


@router.get(path="/application/")
async def application(request: fastapi.Request, token: str = fastapi.Header(None, alias="Authorization")):
    print(f'{request.cookies=}')
    print(f'{request.headers=}')
    print(f'{token=}')
    # if 'authorization' in request.headers:
    #     authorization = request.headers['authorization'].split(' ')[1]
    try:
        return template.TemplateResponse("application.html", {"request": request, 'token': token})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}


@router.get(path="/sign-in/")
async def sign_in(request: fastapi.Request):
    try:
        return template.TemplateResponse(name="sign-in.html", context={"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}






@router.get("/home/")
async def home(request: Request):
    try:
        return template.TemplateResponse("home.html", {"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}

@router.get("/profile/")
async def profile(request: Request):
    try:
        return template.TemplateResponse("profile.html", {"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}




@router.get(path="/dashboard/")
async def dashboard(request: fastapi.Request):
    try:
        return template.TemplateResponse(name="dashboard.html", context={"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}
    
    
@router.get(path="/projects/")
async def projects(request: fastapi.Request):
    try:
        return template.TemplateResponse(name="projects.html", context={"request": request, 'directories': [directory for directory in STORAGE_DIRECTORY_PATH.iterdir()]})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}


@router.post(path='/create/project/')
async def create_project(request: fastapi.Request, project_name: str = fastapi.Form(...)):
    print(f'{request.headers=}')
    print(f'{request.cookies=}')
    
    if not STORAGE_DIRECTORY_PATH.exists():
        return fastapi.Response(status_code=starlette.status.HTTP_404_NOT_FOUND)
    
    project = (STORAGE_DIRECTORY_PATH / project_name)
    
    try:
        if project.exists():
            return fastapi.Response(status_code=starlette.status.HTTP_400_BAD_REQUEST)
        else:
            project.mkdir()
            return fastapi.Response(status_code=starlette.status.HTTP_200_OK)

    except Exception as exception:
        log.exception(msg=str(exception))
        return fastapi.HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.get(path="/works/")
async def works(request: fastapi.Request):
    try:
        return template.TemplateResponse(name="works.html", context={"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}


@router.get(path="/directories/")
async def directories(request: fastapi.Request):
    import os
    
    try:
        user_directories = [directory for directory in os.listdir(STORAGE_DIRECTORY_PATH)]

        return template.TemplateResponse(name="directories.html", context={"request": request, "user_directories": user_directories})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}


@router.get(path="/files/") 
async def files(request: fastapi.Request):
    try:
        return template.TemplateResponse(name="files.html", context={"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}


@router.get(path="/calendar/")
async def calendar(request: fastapi.Request):
    try:
        return template.TemplateResponse(name="calendar.html", context={"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}




@router.get(path="/support/")
async def support(request: fastapi.Request):
    try:
        return template.TemplateResponse(name="support.html", context={"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}


@router.get(path="/settings/")
async def settings(request: fastapi.Request):
    try:
        return template.TemplateResponse(name="settings.html", context={"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}





@router.get(path="/logout/")
async def logout(request: fastapi.Request):
    try:
        return template.TemplateResponse(name="logout.html", context={"request": request})

    except Exception as exception:
        log.exception(msg=str(exception))
        return {"Exception": str(exception)}









