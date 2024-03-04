import fastapi
import fastapi.security
import sqlalchemy.orm
import starlette.status
import uuid

from fastapi import templating
from fastapi import Depends, Request, Response, Header

from typing import Literal, Dict, Any, Annotated




from app.utils import (log, session as _session, TEMPLATE_DIRECTORY_PATH)
from app.schemas import UserAccount as UserAccountSchema, CreateUser
from app.internal.jwt import JWTBearer
from app.maintainer import (
    set_token,
    get_token,
    validate_token,
    validate_user_authentication,
    set_user,
    get_user_by_username,
    set_last_login_date
)



router = fastapi.APIRouter()
authentication_schema = fastapi.security.HTTPBearer()
template = templating.Jinja2Templates(
    directory=TEMPLATE_DIRECTORY_PATH
)



async def session():
    database = _session()
    try:
        yield database

    except Exception as exception:
        log.exception(exception)

    finally:
        database.close()





@router.post(
    path='/signadasads-in/',
    tags=['Autenticación'],
    description='Endpoint para inicio de sesión de usuario.',
    summary='Autenticación del usuario.'
)
async def sign_in(UserAccount: UserAccountSchema, request: fastapi.Request, session: sqlalchemy.orm.Session = fastapi.Depends(session)):

    user_authentication: (tuple | Literal[False]) = validate_user_authentication(
        session=session,
        username=UserAccount.username,
        password=UserAccount.password
    )

    if not user_authentication:
        content = {'message': 'Autenticación fallida.'}

        return fastapi.responses.JSONResponse(status_code=starlette.status.HTTP_401_UNAUTHORIZED, content=content)
    
    user = user_authentication
    user_credential = {}
    user_credential.update(user.get_id())
    user_credential.update(user.get_username())
    user_credential['role_id'] = str(user.role_id)

    set_token(credential=user_credential)

    token: str = get_token()


    set_last_login_date(session=session, user_id=user.id)

    #if (not user_views_control_access or len(user_views_control_access) == 0):
    #    content = {'message': 'Permiso denegado.'}
    #
    #    return fastapi.responses.JSONResponse(status_code=starlette.status.HTTP_403_FORBIDDEN, content=content)

    return {
        'client': request.client.host,
        'user_id': user.id,
        'access_token': token,
    }



@router.post(
    path='/sign-idsaasdn/',
    tags=['Autenticación'],
    description='Endpoint para inicio de sesión de usuario.',
    summary='Autenticación del usuario.'
)
async def sign_ina(UserAccount: UserAccountSchema, request: fastapi.Request, session: sqlalchemy.orm.Session = fastapi.Depends(session)):

    user_authentication: (tuple | Literal[False]) = validate_user_authentication(
        session=session,
        username=UserAccount.username,
        password=UserAccount.password
    )

    if not user_authentication:
        content = {'message': 'Autenticación fallida.'}

        return fastapi.responses.JSONResponse(status_code=starlette.status.HTTP_401_UNAUTHORIZED, content=content)
    
    user = user_authentication
    user_credential = {}
    user_credential.update(user.get_id())
    user_credential.update(user.get_username())
    user_credential['role_id'] = str(user.role_id)

    set_token(credential=user_credential)

    token: str = get_token()


    set_last_login_date(session=session, user_id=user.id)

    if not token:
        content = {'message': 'Permiso denegado.'}

        return fastapi.responses.JSONResponse(status_code=starlette.status.HTTP_403_FORBIDDEN, content=content)


    return {
        'client': request.client.host,
        'user_id': user.id,
        'access_token': token,
    }



@router.post(
    path='/sign-in/',
    tags=['Autenticación'],
    description='Endpoint para inicio de sesión de usuario.',
    summary='Autenticación del usuario.'
)
#async def sign_in(UserAccount: UserAccountSchema, request: fastapi.Request, username: str = fastapi.Form(...), password: str = fastapi.Form(...), session: sqlalchemy.orm.Session = fastapi.Depends(session)):
async def sign_in(UserAccount: UserAccountSchema, request: fastapi.Request, session: sqlalchemy.orm.Session = fastapi.Depends(session)):
    
    user_authentication: (tuple | Literal[False]) = validate_user_authentication(
        session=session,
        username=UserAccount.username,
        password=UserAccount.password
    )

    if not user_authentication:
        content = {'message': 'Autenticación fallida.'}

        return fastapi.responses.JSONResponse(status_code=starlette.status.HTTP_401_UNAUTHORIZED, content=content)
    
    user = user_authentication
    user_credential = {}
    user_credential.update(user.get_id())
    user_credential.update(user.get_username())
    user_credential['role_id'] = str(user.role_id)

    set_token(credential=user_credential)

    token: str = get_token()

    set_last_login_date(session=session, user_id=user.id)

    if not token:
        content = {'message': 'Permiso denegado.'}

        return fastapi.responses.JSONResponse(status_code=starlette.status.HTTP_403_FORBIDDEN, content=content)

    content = {
        'client': request.client.host,
        'user_id': user.id,
        'access_token': token,
    }
    return fastapi.responses.JSONResponse(status_code=starlette.status.HTTP_200_OK, content=content)






@router.post(
    path='/sign-up/',
    status_code=starlette.status.HTTP_201_CREATED,
    tags=['Autenticación'],
    description='Crear usuario.',
    summary='Creación de usuario.',
)
async def sign_up(
    User: CreateUser,
    session: sqlalchemy.orm.Session = fastapi.Depends(session),
    ) -> fastapi.responses.JSONResponse:

    user = get_user_by_username(session=session, username=User.account.username)

    if user:
        content = {'message': 'No se pudo crear el usuario. Por favor intentelo de nuevo.'}

        return fastapi.responses.JSONResponse(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            content=content
        )

    user = set_user(session=session, schema=User)

    content = {'message': 'El usuario ha sido creado.'}
    return fastapi.responses.JSONResponse(
        status_code=starlette.status.HTTP_201_CREATED,
        content=content
    )


@router.post(
    path='/verify/session/',
    tags=['Autenticación'],
    description='Verificar sesión de usuario.',
    summary='Verificación de sesión de usuario.',
    dependencies=[fastapi.Depends(JWTBearer())]
)
async def validate_session(Authorization: str, request: fastapi.Request, session: sqlalchemy.orm.Session = fastapi.Depends(session)) -> fastapi.responses.JSONResponse:
    decoded_token: (fastapi.responses.JSONResponse | Dict[str, Any]) = validate_token(token=Authorization, output=True)

    return {
        'client': request.client.host,
        'user_id': decoded_token['user_id'],
        'user_role_id': decoded_token['role_id'],
        'access_token': Authorization,
    }



################################################################################################################################################################################################

