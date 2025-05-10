from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import logging
from fastapi.middleware.cors import CORSMiddleware

from shared.custom_error import raise_custom_error
from shared.custom_messages import CustomMessages
from shared.custom_response import CustomResponse
from shared.exception_filter import ExceptionFilter
from shared.constants import HTTPCodes,GlobalConstants
from user_module.user_router import user_router

log_file_path = GlobalConstants.log_file_path


load_dotenv()
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path), 
        logging.StreamHandler()     
    ]
)


app = FastAPI(
    title="InterviewMate Backend Service",
    description="Mock Interview Platform",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins to access your app
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
app.add_exception_handler(HTTPException, ExceptionFilter.custom_http_exception_handler)


@app.get("/api/health")
async def health_check():
    try:
        return CustomResponse(
            status_code=HTTPCodes.OK,
            message=CustomMessages.service_working,
            result=None
        )
    except Exception as e:
        raise_custom_error(
            status_code=HTTPCodes.INTERNAL_SERVER_ERROR,
            message=CustomMessages.internal_server_err,
            error=None
        )
    


app.include_router(router=user_router)