from fastapi import HTTPException
from bin.response.response_model import ResponseModel,ErrorResponseModel,FalseResponseModel
from bin.services.hash_password import hash_password,get_digit_code
from bin.services.db_service.redis_service import user_otp_setup,get_user_otp
from bin.services.hash_password import verify_password
from bin.services.jwt_auth import create_token
from bin.services.db_service.user_service import create_new_user,update_user_verified_status,validate_user,update_new_password,\
                                            get_user_details,create_new_invite_user
from bin.controllers.messaging_controller import send_email


class UserManager():
    async def create_user(self ,request):

        digit = next(get_digit_code())
        email_content = {'password': digit}
        await create_new_user(request)
        send_mail_to_user = send_email(to_email=request.email, email_type='public_registration',
                                       contents=email_content)
        await user_otp_setup(request.email,digit)
        if send_mail_to_user:
            return {"status": True,
                    "result": "User registration successful,  Please activate your account before sign in. Activation will sent to your email shortly"}

        return ErrorResponseModel("Email could not be sent, please try again", 403)


    def validate_otp_code(self,request):
        try:
            print('otp -->', request.otp_code)
            otp = get_user_otp(request.email)
            print('otp result-->',otp)
            if otp is not None:
                if int(otp) == request.otp_code:
                    update_user_verified_status(request.email)
                    return ResponseModel(request,'OTP verified')
                else:
                    return ErrorResponseModel('Wrong OTP! Please enter correct OTP', 403)
            else:
                return ErrorResponseModel('User email is wrong',403)

        except Exception as e:
            print(f"Error: {e}")
            raise e

    def sign_in(self,request):
        try:
            user = validate_user(request.email)
            print('user-->', user)
            if user:
                if user.is_admin_approved == 'pending':
                    raise HTTPException(403, {
                        "status": False,
                        "result": "You can’t log in until your account is approved by an admin."
                    })

                elif user.is_admin_approved == 'rejected':
                    raise HTTPException(403, {
                        "status": False,
                        "result": "You can’t log in , your account is rejected by an admin."
                    })
                elif user.is_admin_approved == 'blocked':
                    raise HTTPException(403, {
                        "status": False,
                        "result": "You can’t log in , your account is blocked by an admin."
                    })

                elif user.is_admin_approved == 'approve':
                    if verify_password(pw=request.password, hash_pw=user.password):

                        return {
                            "result": {
                                "id": user.user_id,
                                "full_name": user.full_name,
                                "address": user.address,
                                "phone_number": user.phone_number,
                                "email_address": user.email
                            },
                            "token": create_token(user=user)
                        }

                    else:
                        raise HTTPException(401, {
                            "status": False,
                            "result": "Username or Password Incorrect"
                        })

            raise HTTPException(404, {
                "status": False,
                "result": "No registered user found. Please sign up"
            })

        except Exception as e:
            print(f"Error: {e}")
            raise e

    async def forget_pw(self, request):

        digit = next(get_digit_code())
        email_content = {'password': digit}
        send_mail_to_user = send_email(to_email=request.email, email_type='password_reset',
                                       contents=email_content)
        await user_otp_setup(request.email, digit)
        if send_mail_to_user:
            return {"status": True,
                    "result": "Email sent, please check your email box and enter otp code"}

        return ErrorResponseModel("Email could not be sent, please try again", 403)

    def reset_pw(self, request):
        try:
            update_new_password(request)
            return ResponseModel(request, 'password updated')

        except Exception as e:
            print(f"Error: {e}")
            raise e

    def get_user_profile(self,user_id):
        try:
            print('user_id --->',user_id)
            user = get_user_details(user_id)

            if user:
                return {
                    "status": True,
                    "result":
                        {
                            "uid": user.user_id,
                            "full_name": user.full_name,
                            "email_address": user.email,
                            "phone_number": user.phone_number,
                            "role_id": user.role_id
                        }
                }

        except Exception as e:
            print(f"Error: {e}")
            raise e


    async def invite_user(self ,request):

        email_content = {'password': request.temporary_password}
        await create_new_invite_user(request)
        send_mail_to_user = send_email(to_email=request.email, email_type='user_invitation',
                                       contents=email_content)
        if send_mail_to_user:
            return {"status": True,
                    "result": "User registration invite send successfully"}

        return ErrorResponseModel("Email could not be sent, please try again", 403)




userManager = UserManager()