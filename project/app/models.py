import sqlalchemy
import sqlalchemy.orm
import uuid

from passlib.hash import bcrypt
from app.utils import get_datetime, Base

class UserRoles(Base):
    __tablename__ = 'user_roles'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)


class UserProfiles(Base):
    __tablename__ = 'user_profiles'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    full_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    e_mail = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=get_datetime())
    modification_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=get_datetime())
    

class UserAccounts(Base):
    __tablename__ = 'user_accounts'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    role_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(UserRoles.id), nullable=False)
    profile_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(UserProfiles.id), unique=True, nullable=False)

    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=get_datetime())
    last_login_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    
    role = sqlalchemy.orm.relationship('UserRoles', backref='user', uselist=False)
    profile = sqlalchemy.orm.relationship('UserProfiles', backref='user', uselist=False)

    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True, nullable=False)

    def validate_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)

    def get_id(self) -> dict[str, str]:
        return {'user_id': self.id}

    def get_username(self) -> dict[str, str]:
        return {'username': self.username}


class UserActions(Base):
    __tablename__ = 'user_actions'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class UserComments(Base):
    __tablename__ = 'user_comments'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(UserAccounts.id), nullable=False)

    account_relation = sqlalchemy.orm.relationship('UserAccounts', backref='comment', uselist=False, foreign_keys=[user_id])

    text = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True, nullable=False)

    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=get_datetime())
    modification_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=get_datetime())
