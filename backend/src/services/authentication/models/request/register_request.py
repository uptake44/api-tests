from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    username: str
    password: str
    password_repeat: str
    email: EmailStr
