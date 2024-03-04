import pathlib
import datetime
import logging
import pytz
import os
import dotenv
dotenv.load_dotenv()



DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
ZONE = os.getenv('TZ')
TIMEZONE = pytz.timezone(zone=ZONE)

API_TITLE = 'API'
API_DESCRIPTION = 'API documentation'
API_VERSION = 'v1'
API_HOST = '0.0.0.0'
API_PORT = 7500



def connect(path: pathlib.Path):
    import sqlite3

    connection = sqlite3.connect(database=path)
    
    return connection.close()
    

def get_datetime() -> datetime.datetime:
    return datetime.datetime.now(tz=TIMEZONE)


INTERNAL_DIRECTORY_NAME = 'internal'
INTERNAL_DIRECTORY_PATH = (pathlib.Path(__file__).parent.absolute() / '{0}'.format(INTERNAL_DIRECTORY_NAME))

DATABASE_DIRECTORY_NAME = 'storage'
DATABASE_DIRECTORY_PATH = (INTERNAL_DIRECTORY_PATH / '{0}'.format(DATABASE_DIRECTORY_NAME))

if not DATABASE_DIRECTORY_PATH.exists():
    DATABASE_DIRECTORY_PATH.mkdir()
    
    
DATABASE_FILE_NAME = 'internal.db'
DATABASE_FILE_PATH = (DATABASE_DIRECTORY_PATH / '{0}'.format(DATABASE_FILE_NAME))

if not DATABASE_FILE_PATH.exists():
    connect(path=DATABASE_FILE_PATH)


TEMPLATE_DIRECTORY_NAME = 'templates'
TEMPLATE_DIRECTORY_PATH = (pathlib.Path(__file__).parent.absolute() / '{0}'.format(TEMPLATE_DIRECTORY_NAME))


STATIC_DIRECTORY_NAME = 'static'
STATIC_DIRECTORY_PATH = (pathlib.Path(__file__).parent.absolute() / '{0}'.format(STATIC_DIRECTORY_NAME))

STORAGE_DIRECTORY_NAME = 'storage'
STORAGE_DIRECTORY_PATH = (pathlib.Path(__file__).parent.absolute() / '{0}'.format(STORAGE_DIRECTORY_NAME))



LOG_DIRECTORY_PATH = (pathlib.Path(__file__).parent.absolute() / 'logs')
LOG_FILE_NAME = '{0}.log'.format(get_datetime().strftime('%d_%m_%Y'))
LOG_FILE_PATH = (LOG_DIRECTORY_PATH / LOG_FILE_NAME)

LOG_MESSAGE_FORMAT = '%(asctime)-20s %(levelname)-10s %(module)s.%(funcName)s: %(message)s'
LOG_DATE_FORMAT = '%d/%m/%Y %I:%M:%S %p'
LOG_FORMATTER = logging.Formatter(fmt=LOG_MESSAGE_FORMAT, datefmt=LOG_DATE_FORMAT)



API_USERS = '/api/{0}'.format(API_VERSION)
API_STATIC = '/api/{0}/'.format(STATIC_DIRECTORY_NAME)



ALL = ['*']
ALLOWED = True






from app.log import log

if not LOG_DIRECTORY_PATH.exists():
    LOG_DIRECTORY_PATH.mkdir()
    
LOG_FILE_HANDLER = logging.FileHandler(filename=LOG_FILE_PATH, encoding='utf-8', mode='+a')
LOG_FILE_HANDLER.setFormatter(LOG_FORMATTER)

log.addHandler(LOG_FILE_HANDLER)
log.debug(
    msg=(
        TIMEZONE,
        API_TITLE,
        API_DESCRIPTION,
        API_VERSION,
        API_HOST,
        API_PORT,
        TEMPLATE_DIRECTORY_NAME,
        TEMPLATE_DIRECTORY_PATH,
        STATIC_DIRECTORY_NAME,
        STATIC_DIRECTORY_PATH,
        STORAGE_DIRECTORY_NAME,
        STORAGE_DIRECTORY_PATH,
        
        LOG_DIRECTORY_PATH,
        LOG_FILE_NAME,
        LOG_FILE_PATH,
        LOG_MESSAGE_FORMAT,
        LOG_DATE_FORMAT,
        LOG_FORMATTER,
        API_USERS,
        API_STATIC,
        ALL,
        ALLOWED
    )
)


from app.internal.database import (session, Base, engine)
from app.models import UserActions, UserProfiles, UserRoles, UserAccounts, UserComments

Base.metadata.create_all(bind=engine)
