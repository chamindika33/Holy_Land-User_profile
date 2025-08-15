from fastapi import APIRouter,Depends
from bin.requests.admin_request import AdminApproveRequest,AllUserData
from bin.controllers.admin_controller import adminManager

router = APIRouter(
    prefix="/holy-land",
    tags=["Admin"]
)


@router.post("/admin-approve")
def admin_approve(request: AdminApproveRequest):
    return adminManager.approve_user(request)

@router.post("/get-all-user-list")
def get_all_user_list(request:AllUserData):
    return adminManager.get_all_user_list(request)