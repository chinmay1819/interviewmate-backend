from pydantic import BaseModel,EmailStr,constr,Field


class UserRegister(BaseModel):
    name: constr(strip_whitespace=True,min_length=2,max_length=50) = Field(...,example="John Doe")
    email: EmailStr = Field(...,example="john.doe@example.com")
    password: constr(min_length=8,max_length=128) = Field(...,example="strongpassword@123")


class UserLogin(BaseModel):
    email:EmailStr = Field(...,example="john.doe@example.com")
    password: constr(min_length=8,max_length=128) = Field(...,example="yourpassword")
    