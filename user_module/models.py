from typing import List,Literal
from pydantic import BaseModel,EmailStr,constr,Field,HttpUrl,Field


class UserRegister(BaseModel):
    name: constr(strip_whitespace=True,min_length=2,max_length=50) = Field(...,example="John Doe")
    email: EmailStr = Field(...,example="john.doe@example.com")
    password: constr(min_length=8,max_length=128) = Field(...,example="strongpassword@123")


class UserLogin(BaseModel):
    email:EmailStr = Field(...,example="john.doe@example.com")
    password: constr(min_length=8,max_length=128) = Field(...,example="yourpassword")
    

class Experience(BaseModel):
    years:int = Field(..., ge=0,example=2)
    months:int = Field(...,ge=0,le=11,example=0)


class UserProfileDetails(BaseModel):
    role:Literal["candidate","interviewer"] = Field(...,example="candidate") # It should have two options either it can be candidate or interviewer
    experience:Experience
    tech_stack:List[str] = Field(...,example=["Python","FastAPI","AWS","Angular"])
    domain:Literal["Frontend", "Backend", "Data Engineering", "Data Science", "AI Engineering", "Machine Learning", "DevOps", "MLOps", "Other"] = Field(...,example="Backend") 

    previous_work_description:str = Field(..., example="Worked on backend microservices in Python")
    current_company: str = Field(..., example="Google")
    linkedin_profile_link: HttpUrl = Field(...,example="https://www.linkedin.com/in/your-profile")