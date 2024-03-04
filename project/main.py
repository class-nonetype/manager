import os
import pathlib


os.chdir(path=pathlib.Path(__file__).parent.absolute())

import fastapi
import fastapi.middleware.cors
import fastapi.staticfiles

from app.utils import (
    TIMEZONE,
    
    API_TITLE,
    API_DESCRIPTION,
    API_HOST,
    API_VERSION,
    API_PORT,

    API_STATIC,

    STORAGE_DIRECTORY_PATH,
    
    STATIC_DIRECTORY_NAME,
    STATIC_DIRECTORY_PATH,


    ALL,
    ALLOWED
)
from app.routers import (authentication, views)




app = fastapi.FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)
app.timezone = TIMEZONE

app.include_router(router=views.router)
app.include_router(router=authentication.router, prefix='/auth')



if not STORAGE_DIRECTORY_PATH.exists():
    STORAGE_DIRECTORY_PATH.mkdir()

app.mount(
    path=API_STATIC,
    app=fastapi.staticfiles.StaticFiles(directory=STATIC_DIRECTORY_PATH),
    name=STATIC_DIRECTORY_NAME
)





'''
Agrega el middleware CORS para permitir solicitudes desde cualquier origen ('*').
También se permite el uso de credenciales, todos los métodos y headers.
'''
app.add_middleware(
    middleware_class = fastapi.middleware.cors.CORSMiddleware,
    allow_origins = ALL,
    allow_credentials = ALLOWED,
    allow_methods = ALL,
    allow_headers = ALL
)



if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(app=app, host=API_HOST, port=API_PORT)

