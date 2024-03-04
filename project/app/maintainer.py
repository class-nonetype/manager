import datetime
import jwt
import fastapi
import uuid
import sqlalchemy.orm


from app.utils import get_datetime, SECRET_KEY, log
from app.models import UserAccounts as UserAccountsModel, UserProfiles as UserProfilesModel
from app.schemas import CreateUser

from passlib.hash import bcrypt
from typing import Literal


def set_expiration_date(hours: int) -> str:
    expiration_date = datetime.datetime.now() + datetime.timedelta(hours=hours)
    return expiration_date.strftime('%Y-%m-%d %H:%M:%S.%f%z')


def set_token(credential: dict) -> str:
    global token
    token = jwt.encode(payload={**credential, 'expires': set_expiration_date(hours=8)}, key=SECRET_KEY, algorithm='HS256')


def get_token() -> str:
    return token


def validate_token(token: str, output=False):
    try:
        decoded_token = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        expiration_date = datetime.datetime.strptime(decoded_token['expires'], '%Y-%m-%d %H:%M:%S.%f%z')
        current_date = get_datetime(timezone=expiration_date.tzinfo)

        if (output and expiration_date < current_date):
            return fastapi.responses.JSONResponse(content={'message': 'Token expirado'}, status_code=401)

        return decoded_token
    except jwt.exceptions.DecodeError:
        return fastapi.responses.JSONResponse(content={'message': 'Token inválido'}, status_code=401)


def validate_token_(token: str, output=False):
    decoded_token = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
    expiration_date = datetime.datetime.strptime(decoded_token['expires'], '%Y-%m-%d %H:%M:%S.%f%z')
    current_date = get_datetime(timezone=expiration_date.tzinfo)

    if (output and expiration_date < current_date):
        return False
    return True

def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        expiration_date = datetime.datetime.strptime(decoded_token["expires"], "%Y-%m-%d %H:%M:%S.%f%z")
        current_date = datetime.datetime.now(expiration_date.tzinfo)

        if (expiration_date > current_date):
            return decoded_token

    except jwt.exceptions.DecodeError:
        return fastapi.responses.JSONResponse(content={'message': 'Token inválido'}, status_code=401)



















def set_user_profile(**kwargs):
    user_profile = UserProfilesModel(
        id=kwargs.get('id'),
        full_name=kwargs.get('full_name'),
        e_mail=kwargs.get('e_mail')
    )
    return user_profile




def get_user_profile_by_account_id(session: sqlalchemy.orm.Session, account_id: uuid.UUID):
    return session.query(UserProfilesModel).\
        join(UserAccountsModel, UserProfilesModel.id == UserAccountsModel.profile_id).\
        filter(UserAccountsModel.id == account_id).\
        first()





def get_user_by_username(session: sqlalchemy.orm.Session, username: str):
    return session.query(UserAccountsModel).filter(UserAccountsModel.username==username).first()


def get_user_by_account_id(session: sqlalchemy.orm.Session, account_id: uuid.UUID):
    return session.query(UserAccountsModel).filter(UserAccountsModel.id==account_id).first()


def set_last_login_date(session: sqlalchemy.orm.Session, user_id: uuid.UUID) -> None:
    session.query(UserAccountsModel).filter(UserAccountsModel.id == user_id).update(
        {'last_login_date': get_datetime()}
    )
    return session.commit()



def set_user_account(**kwargs):
    user_account = UserAccountsModel(
        id=kwargs.get('id'),
        role_id=kwargs.get('role_id'),
        profile_id=kwargs.get('profile_id'),
        username=kwargs.get('username'),
        password=kwargs.get('password')
    )
    return user_account




def set_user(session: sqlalchemy.orm.Session, schema: CreateUser) -> UserAccountsModel:
    try:
        user_profile: UserProfilesModel = set_user_profile(
            id=str(uuid.uuid4()),
            full_name=schema.profile.full_name,
            e_mail=schema.profile.e_mail
        )
        session.add(user_profile)
        session.commit()

        user_account: UserAccountsModel = set_user_account(
            id=str(uuid.uuid4()),
            role_id=schema.role.id,
            profile_id=user_profile.id,
            username=schema.account.username,
            password=bcrypt.hash(schema.account.password)
        )
        session.add(user_account)
        session.commit()
        
        return user_account

    except sqlalchemy.exc.IntegrityError as exception:
        session.rollback()

        log.exception(msg=exception)
        raise exception

    except Exception as exception:
        session.rollback()

        log.exception(msg=exception)
        raise exception


def validate_user_authentication(session: sqlalchemy.orm.Session, username: str, password: str) -> (tuple | Literal[False]):
    user = get_user_by_username(session=session, username=username)

    if (not user or not user.validate_password(password) or not user.active):
        return False

    return user


def validate_user_session(session: sqlalchemy.orm.Session, account_id: uuid.UUID):
    user = get_user_by_account_id(session=session, account_id=account_id)
    
    if (not user or not user.active):
        return False
    return user