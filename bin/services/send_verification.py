import os
import configparser

from bin.services.email_service import send_e_mail
from bin.templates.activation_email import PasswordEmail

config = configparser.RawConfigParser()
config.read(os.path.abspath(os.curdir) + '/.cfg')


def send_verification_email(contents):
    email = PasswordEmail(
        subject='Lets Talk Account Activation',
        salutation='Dear User',
        paragraph='Thank you for registering with ' + str(config['ENVIRONMENT']['APP_NAME']) +
                  '. Please use the below password to login using your email.',
        recipient=contents['send_to'],
        code=contents['password']
    )

    return send_e_mail(next(email()))

def send_public_acc_verification_email(contents):
    email = PasswordEmail(
        subject='Holy Land Account Activation',
        salutation='Dear User',
        paragraph='Thank you for registering with holyland.' 
                  '. Please use the below OTP to continue user activation.',
        recipient=contents['send_to'],
        code=contents['password']
    )

    return send_e_mail(next(email()))

def send_user_invitation_email(contents):
    email = PasswordEmail(
        subject='Holy Land Account Invitation',
        salutation='Dear User',
        paragraph='You have been invited Holy Land account registration.' 
                  '. Please use the below Password to activate your account.',
        recipient=contents['send_to'],
        code=contents['password']
    )

    return send_e_mail(next(email()))

def send_password_reset_email(contents):
    email = PasswordEmail(
        subject='Holy Land Account Password Reset',
        salutation='Dear User',
        paragraph='A password reset was requested for your Holy Land Account.'
                  ' Please use the below OTP to reset your password.',
        recipient=contents['send_to'],
        code=contents['password']
    )

    return send_e_mail(next(email()))




# def send_varification_sms(user: User) -> User:
#     digit = next(get_digit_code())
#     message = OTPMesssage(digit, int(otp_valid))
#
#     otp = OneTimePassword(
#         digit_code=digit, digit_code_created=datetime.now(), digit_code_attempts=0)
#     user.new_otp.append(otp)
#     sms = SMSGateway().set_body(message)
#     delivered = sms.send_to(user.original_primary_contact)
#     if delivered:
#         return user
#
#     else:
#         return HTTPException(400, {"status": False, "result": "Unable to save user account"})
