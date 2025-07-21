from bin.db.postgresDB import db_connection
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import delete, update, exists, func, and_
from bin.models import pg_models
from sqlalchemy.exc import SQLAlchemyError
from bin.response.response_model import ErrorResponseModel
from bin.services.hash_password import hash_password
from datetime import datetime, timezone

db: Session = next(db_connection())


async def create_new_user(request):
    try:
        data = pg_models.User(
            full_name=request.full_name,
            password=hash_password(request.password),
            address = request.address,
            email=request.email,
            phone_number=request.phone_number,
            email_verified=False,
            role_id=request.role_id

        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data.user_id

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)


def update_user_verified_status(email):
    try:
        update_query = update(pg_models.User).where(
                            pg_models.User.email == email
                        ).values(
                            email_verified = True
                        )
        result = db.execute(update_query)
        db.commit()

        rows_upadted = result.rowcount
        print("rows",rows_upadted)
        return rows_upadted
    except SQLAlchemyError as e:
        db.rollback()
        return 0


def update_new_password(request):
    try:
        update_query = update(pg_models.User).where(
                            pg_models.User.email == request.email
                        ).values(
                            password = hash_password(request.password)
                        )
        result = db.execute(update_query)
        db.commit()

        rows_upadted = result.rowcount
        print("rows",rows_upadted)
        return rows_upadted
    except SQLAlchemyError as e:
        db.rollback()
        return 0



def validate_user(email):
    try:
        data = db.query(
                pg_models.User
            ).filter(
                pg_models.User.email == email
            ).first()
        return data

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)