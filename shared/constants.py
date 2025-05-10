class HTTPCodes:
    # 2xx Success
    OK = 200  # Request succeeded
    CREATED = 201  # Resource successfully created
    ACCEPTED = 202  # Request accepted for processing, but not completed
    NO_CONTENT = 204  # Request succeeded, but no content to return

    # 3xx Redirection
    MOVED_PERMANENTLY = 301  # Resource moved permanently
    FOUND = 302  # Resource found, typically used for redirection
    NOT_MODIFIED = 304  # Resource has not been modified since last request

    # 4xx Client Errors
    BAD_REQUEST = 400  # Malformed request
    UNAUTHORIZED = 401  # Authentication required
    FORBIDDEN = 403  # Authenticated but not authorized
    NOT_FOUND = 404  # Resource not found
    METHOD_NOT_ALLOWED = 405  # Method not allowed on resource
    CONFLICT = 409  # Conflict, e.g. duplicate data
    UNPROCESSABLE_ENTITY = 422  # Validation error (used by FastAPI for validation failures)

    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = 500  # Generic server error
    NOT_IMPLEMENTED = 501  # Functionality not implemented
    BAD_GATEWAY = 502  # Invalid response from upstream server
    SERVICE_UNAVAILABLE = 503  # Server temporarily unavailable
    GATEWAY_TIMEOUT = 504  # Upstream server didn't respond in time



class GlobalConstants:
    log_file_path = "app.log"
    jwt_algorithm = "HS256"