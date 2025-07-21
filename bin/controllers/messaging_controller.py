# from services.email_service import send_e_mail
from bin.services.send_verification import send_verification_email, send_password_reset_email,send_public_acc_verification_email


def send_email(to_email, email_type, contents, method=None):
    print('send mail')
    contents['send_to'] = to_email

    if email_type == 'registration':
        if 'password' in contents:
            return send_verification_email(contents=contents)

    if email_type == 'password_reset':
        if 'password' in contents:
            return send_password_reset_email(contents=contents)

    if email_type == 'public_registration':
        if 'password' in contents:
            return send_public_acc_verification_email(contents=contents)



    return True

