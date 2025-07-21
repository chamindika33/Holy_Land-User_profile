from pydantic import BaseModel, EmailStr, validator, field_validator, Field
from bin.services.custom_validations import email_validation,email_available,mobile_validation,mobile_available,check_email_availablity


class NewUser(BaseModel):
    full_name: str
    email: EmailStr
    address: str
    phone_number: str
    password: str
    role_id: int

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        email_validation(value)
        email_available(value)
        return value

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value):
        mobile_validation(value)
        mobile_available(value)
        return value


class UserActivationRequest(BaseModel):
    email: EmailStr = Field(...)
    otp_code: int = Field(...)

    @field_validator('email')
    def func(cls, value):
        method = None
        if isinstance(value, str):
            method = 'email'
            email_validation(value)

        if isinstance(value, type(None)):
            raise ValueError('Email required')

        setattr(cls, 'method', method)
        return value

class ForgetPWRequest(BaseModel):
    email: EmailStr = Field(...)

    @field_validator('email')
    def func(cls, value):
        method = None
        if isinstance(value, str):
            method = 'email'
            email_validation(value)
            check_email_availablity(value)

        if isinstance(value, type(None)):
            raise ValueError('Please enter valid email address')

        setattr(cls, 'method', method)
        return value

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(...)

    @field_validator('email')
    def func(cls, value):
        method = None
        if isinstance(value, str):
            method = 'email'
            email_validation(value)

        if isinstance(value, type(None)):
            raise ValueError('Email required')

        setattr(cls, 'method', method)
        return value