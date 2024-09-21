import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, Response

from app.common.utils import get_env_variable
app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code >= 500:
        logging.error(f"HTTP error occurred: {exc.detail}", exc_info=True)
    else:
        logging.warning(f"HTTP warning occurred: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Error occurred: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


# get environment variables - get_env_variable loads the .env file for the first time
try:
    ENV = get_env_variable("ENV")

except ValueError as val_err:
    log_msg = f"Could not get env var = {val_err}"
    logging.error(log_msg)
    raise val_err
except Exception as err:
    log_msg = f"Error occured while getting env var = {err}"
    logging.error(log_msg)
    raise err


# CORS settings
origins = [
    "http://localhost:3000",
]


@app.get("/")
def root():
    return {"message": "OK"}


# health check
@app.get("/health")
def health_check():
    import socket
    from datetime import datetime

    return {
        "status": "ok",
        "hostname": socket.gethostname(),
        "host": get_env_variable("CONTAINER_NAME", "NO_CONTAINER_NAME"),
        "ts": str(datetime.now().timestamp()),
    }

# handle favicon requests with an empty response
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)  # no Content status