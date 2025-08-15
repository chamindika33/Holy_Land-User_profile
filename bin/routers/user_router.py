from fastapi import FastAPI,APIRouter,Query,Depends
from fastapi.exceptions import HTTPException
from bin.middleware.user_middleware import Authorization
from bin.requests.user_requests import NewUser,UserActivationRequest,UserLoginRequest,ForgetPWRequest,\
                            InviteUser
from bin.controllers.user_controller import userManager

router = APIRouter(
    prefix="/holy-land",
    tags=["User"]
)

@router.post("/create-user")
async def create_new_user(request:NewUser):
    return await userManager.create_user(request)

@router.post("/verify-otp")
def verify_otp(request: UserActivationRequest):
    return userManager.validate_otp_code(request)

@router.post('/login')
def sign_in_user(request: UserLoginRequest):
    return userManager.sign_in(request)

@router.get('/profile')
def show_user_profile(authentication=Depends(Authorization())):
    return userManager.get_user_profile(user_id=authentication.sub)

@router.post('/forget-password')
async def forget_passowrd(request: ForgetPWRequest):
    return await userManager.forget_pw(request)

@router.post('/set-new-password')
def set_new_password(request: UserLoginRequest):
    return userManager.forget_pw(request)

@router.post('/invite')
async def set_new_password(request:InviteUser):
    return await userManager.invite_user(request)

