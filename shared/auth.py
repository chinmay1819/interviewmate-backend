import logging
import os
from fastapi import Depends
from fastapi.security import APIKeyHeader
import jwt


from shared.custom_error import raise_custom_error
from shared.custom_messages import CustomMessages
from shared.db_connection import db
from shared.constants import GlobalConstants, HTTPCodes

bearer_scheme = APIKeyHeader(name="Authorization")

class AuthService:

    @staticmethod
    async def get_current_user(token:str=Depends(bearer_scheme)):
        try:
            
            scheme, _, token = token.partition(" ")
            if scheme.lower() != "bearer":
                logging.info("Please add Bearer before the token !")
                raise_custom_error(
                    status_code=HTTPCodes.BAD_REQUEST,
                    error=CustomMessages.invalid_token,
                    message=CustomMessages.add_bearer
                )


            secret_key = os.getenv("SECRET_KEY")
            algorithm = GlobalConstants.jwt_algorithm

            # decode the token using secret key 
            payload = jwt.decode(token,secret_key,algorithms=[algorithm])
            user_email = payload["email"]

            return user_email
        
        except jwt.PyJWTError as jwt_err:
            logging.error(f"Token decoding error: {jwt_err}")
            raise ValueError("Invalid token")

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise Exception("Could not validate user")