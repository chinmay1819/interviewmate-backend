import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class ExceptionFilter:

    @staticmethod
    def parse_nested_error(error):
        """
        Recursively parse nested error messages into a dictionary.
        Handles JSON-like strings and gracefully degrades for malformed inputs.
        """
        if isinstance(error, str):
            try:
                # Find the JSON part in the string
                nested_error_start = error.find("{")
                if nested_error_start != -1:
                    json_string = error[nested_error_start:]
                    parsed_error = json.loads(json_string.replace("'", '"').replace("None", "null"))
                    return ExceptionFilter.parse_nested_error(parsed_error)
            except Exception:
                pass  # If parsing fails, return the raw string
        elif isinstance(error, dict):
            # Recursively process any nested "error" field
            if "error" in error and isinstance(error["error"], (str, dict)):
                error["error"] = ExceptionFilter.parse_nested_error(error["error"])
        return error

    @staticmethod
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        try:
            if isinstance(exc.detail, dict) and "status_code" in exc.detail and "error" in exc.detail:
                # Extract and process the error field if nested
                parsed_error = ExceptionFilter.parse_nested_error(exc.detail.get("error"))
                
                return JSONResponse(
                    status_code=exc.detail["status_code"],
                    content={
                        "status_code": exc.detail["status_code"],
                        "message": exc.detail["message"],
                        "error": parsed_error
                    }
                )
            
            else:
                # Fallback for generic errors
                return JSONResponse(
                    status_code=exc.status_code,
                    content={
                        "status_code": exc.status_code,
                        "message": exc.detail if isinstance(exc.detail, str) else "An error occurred.",
                        "error": None
                    }
                )
        except Exception as e:
            # Handle any unexpected issues during error processing
            return JSONResponse(
                status_code=500,
                content={
                    "status_code": 500,
                    "message": "An error occurred while processing the error.",
                    "error": str(e)
                }
            )
