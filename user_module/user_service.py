import logging
import os
import bcrypt
from datetime import datetime,timedelta
import jwt
import pytz

from user_module.exceptions import DatabaseError, ProvidedValueError
from user_module.models import UserProfileDetails, UserRegister,UserLogin
from shared.db_connection import db
from pymongo.errors import PyMongoError


class UserService:
    def __init__(self):
        self.user_collection = db["user"]
        

    async def signup_user(self,user:UserRegister):
        try:
            email = user.email
            
            existing_user = self.user_collection.find_one({"email":email})
            if existing_user:
                raise ValueError("User already exists")

            password = bcrypt.hashpw(user.password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            # hash the password 
            self.user_collection.insert_one({
                "name":user.name,
                "email":user.email,
                "password":password
            })

            return True
            
        except ValueError as ve:
            logging.error(str(ve))
            raise ProvidedValueError(str(ve))
        
        except PyMongoError as db_error:
            logging.error(str(db_error))
            raise DatabaseError("Unable to interact with database at this moment")
        
        except Exception as e:
            raise Exception("Unexpected error while registering user")
        
    

    def create_jwt_token(self,data:dict):
        to_encode = data.copy()
        expire = datetime.now(pytz.UTC) + timedelta(days=2)
        
        to_encode["exp"] = expire

        secret_key = os.getenv("SECRET_KEY")
        encoded_jwt = jwt.encode(payload=to_encode,key=secret_key,algorithm="HS256")
        
        return encoded_jwt
       


    async def login(self,user:UserLogin):
        try:
            stored_user = self.user_collection.find_one({"email":user.email})
            
            if not stored_user:
                raise ValueError("User does not exist")
            
            stored_password = stored_user["password"]

            if not bcrypt.checkpw(user.password.encode('utf-8'),stored_password.encode('utf-8')):
                raise ValueError("Incorrect email or password")
            
            jwt_token = self.create_jwt_token(data={
                "email": stored_user["email"]
            })

            return jwt_token
        
        except ValueError as ve:
            logging.error(str(ve))
            raise ProvidedValueError(str(ve))
        except PyMongoError as db_error:
            logging.error(str(db_error))
            raise DatabaseError("Unable to interact with database at this moment")
        except Exception as e:
            raise Exception("Unexpected error while logging in...")
        

    

    async def create_user_profile(self,user_profile_details:UserProfileDetails,user_email:str):
        try:
            profile_details = {
                "role":user_profile_details.role,
                "experience":{
                    "years":user_profile_details.experience.years,
                    "months":user_profile_details.experience.months
                },
                "tech_stack":user_profile_details.tech_stack,
                "domain":user_profile_details.domain,
                "previous_work_description":user_profile_details.previous_work_description,
                "current_company":user_profile_details.current_company,
                "linkedin_profile_link":str(user_profile_details.linkedin_profile_link)
            }
            self.user_collection.update_one(
                {"email":user_email},
                {"$set":{"profile_details":profile_details}}
            )
            
            return True

        except ValueError as ve:
            logging.error(str(ve))
            raise ProvidedValueError(str(ve))
        except PyMongoError as db_err:
            logging.error(str(db_err))
            raise DatabaseError("Unable to interact with database at this moment")
        except Exception as e:
            logging.error(str(e))
            raise Exception("Unexpected error while creating user profile")