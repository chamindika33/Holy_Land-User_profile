from fastapi import HTTPException

from bin.response.response_model import ResponseModel,ErrorResponseModel,FalseResponseModel
from bin.services.db_service.admin_service import update_user_status,get_all_users


class AdminManager():
    def approve_user(self,request):
        result = update_user_status(request)
        if result == 0:
            return ErrorResponseModel(
                message="Approval Failed: Something went wrong while approving the user. Please try again.",
                status_code=400
            )

        return ResponseModel(
            request,
            message="User Approved: The user has been successfully approved and notified to log in."
        )

    def get_all_user_list(self, request):
        try:
            offset = (request.page_number - 1) * request.record_per_page
            print('offset-->', offset)
            data = get_all_users(offset, request.record_per_page)
            result = {
                'data': data['data'],
                'page_number': request.page_number,
                'record_per_page': request.record_per_page,
                'No of records': data['total_records']
            }

            return ResponseModel(result, "retrieved data")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e), 400)

adminManager = AdminManager()