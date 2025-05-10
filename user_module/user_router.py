from fastapi import APIRouter, Depends
from pymongo.errors import PyMongoError
from shared.auth import AuthService
from shared.custom_messages import CustomMessages
from shared.constants import HTTPCodes
from shared.custom_response import CustomResponse
from shared.custom_error import raise_custom_error
from user_module.exceptions import DatabaseError, ProvidedValueError
from user_module.models import UserLogin, UserProfileDetails, UserRegister
from user_module.user_service import UserService

user_router = APIRouter(prefix="/api/user",tags=["User"])

@user_router.post("/register")
async def register_user(user:UserRegister):
    try:
        service = UserService()
        await service.signup_user(user=user)
        
        return CustomResponse(
            status_code=HTTPCodes.CREATED,
            message=CustomMessages.user_created,
            result=None
        )
    
    except ProvidedValueError as ve:
        raise_custom_error(
            status_code=HTTPCodes.CONFLICT,
            message=CustomMessages.user_not_created,
            error=ve
        )

    except DatabaseError as dberr:
        raise_custom_error(
            status_code=HTTPCodes.INTERNAL_SERVER_ERROR,
            message=CustomMessages.user_not_created,
        )

    except Exception as e:
        raise_custom_error(
            status_code=HTTPCodes.INTERNAL_SERVER_ERROR,
            message=CustomMessages.internal_server_err
        )
    


@user_router.post("/login")
async def login(user:UserLogin):
    try:
        service = UserService()
        result = await service.login(user=user)
        
        return CustomResponse(
            status_code=HTTPCodes.ACCEPTED,
            message=CustomMessages.login_success,
            result=result
        )
    
    except ProvidedValueError as ve:
        raise_custom_error(
            status_code=HTTPCodes.UNAUTHORIZED,
            message=CustomMessages.invalid_credentials,
        )

    except DatabaseError as db_error:
        raise_custom_error(
            status_code=HTTPCodes.INTERNAL_SERVER_ERROR,
            message=CustomMessages.internal_server_err
        )
    except Exception as e:
        raise_custom_error(
            status_code=HTTPCodes.INTERNAL_SERVER_ERROR,
            message=CustomMessages.internal_server_err
        )



@user_router.post("/create-profile")
async def create_user_profile(user_profile:UserProfileDetails,email:str = Depends(AuthService.get_current_user)):
    try:
        service = UserService()
        
        result = await service.create_user_profile(user_profile_details=user_profile,user_email=email)
        return CustomResponse(
            status_code=HTTPCodes.CREATED,
            message=CustomMessages.profile_created,
            result=result
        )
    
    except ProvidedValueError as pve:
        raise_custom_error(
            status_code=HTTPCodes.BAD_REQUEST,
            message=CustomMessages.profile_not_created,
            error=str(pve)
        )
    
    except DatabaseError as db_error:
        raise_custom_error(
            status_code=HTTPCodes.INTERNAL_SERVER_ERROR,
            message=CustomMessages.internal_server_err
        )
    
    except Exception as e:
        print(str(e))
        raise_custom_error(
            status_code=HTTPCodes.INTERNAL_SERVER_ERROR,
            message=CustomMessages.internal_server_err
        )

