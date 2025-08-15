from bin.db.postgresDB import db_connection
from sqlalchemy.orm import Session
from sqlalchemy import  update
from bin.models import pg_models
from sqlalchemy.exc import SQLAlchemyError
from bin.response.response_model import ResponseModel,ErrorResponseModel,FalseResponseModel


db: Session = next(db_connection())


def update_user_status(request):
    try:
        update_query = update(pg_models.User).where(
            pg_models.User.user_id == request.user_id
        ).values(
            is_admin_approved = request.admin_status
        )
        result = db.execute(update_query)
        db.commit()

        rows_upadted = result.rowcount
        print("rows", rows_upadted)
        return rows_upadted

    except SQLAlchemyError :
        db.rollback()
        return 0

def get_all_users(offset,record_per_page):
    try:
        data = db.query(
            pg_models.User
        ).order_by(pg_models.User.user_id.asc())
        data = data.offset(offset).limit(record_per_page).all()

        total_records = db.query(pg_models.User).count()

        result = {
            "total_records": total_records,
            "data": data
        }

        return result

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)