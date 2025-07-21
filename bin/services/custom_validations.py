import re
import string

from bin.db.postgresDB import db_connection
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, exists, and_
from bin.models import pg_models
from bin.models.pg_models import User
from sqlalchemy.exc import SQLAlchemyError
from bin.response.response_model import ErrorResponseModel

db: Session = next(db_connection())


async def check_user_email(email):
    query = db.query(exists().where(
        and_(
            pg_models.User.email == email
        )
    )).scalar()

    return query


def email_validation(value: str):
    if not value:
        raise ValueError('Email address required')

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, value):
        raise ValueError('Invalid email address')
    return value


def email_available(value: str):
    exists_query = db.query(User).filter(
        User.email == value.lower()
    ).first()
    if exists_query:
        raise ValueError('This email already in use')
    return value.lower()

def check_email_availablity(value: str):
    exists_query = db.query(User).filter(
        User.email == value.lower()
    ).first()
    if exists_query:
        return value.lower()
    else:
        raise ValueError('we could not find the account with that email ')


def mobile_validation(value: str):
    pattern = r"^[0-9]{9,}$"
    if not re.match(pattern, str(value)):
        raise ValueError('Valid mobile number is required')
    return value


def mobile_available(value: str):
    user = db.query(User).filter(User.phone_number == str(value)).first()
    if user:
        if user.email_verified != True:
            db.query(User).filter_by(user_id=user.user_id).delete()
            db.commit()
            return value
        raise ValueError('This mobile number already in use')
    return value
