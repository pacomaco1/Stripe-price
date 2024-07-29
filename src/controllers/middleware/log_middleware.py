import logging
import traceback

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        logging.info(f"Request path: {request.url.path} | Method: {request.method}")
        try:
            response = await call_next(request)
            logging.info(f"Response status: {response.status_code}")
            return response
        except Exception as error:
            logging.error(f"An error occurred: {type(error).__name__}; {str(error)}", exc_info=True)
            tb_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": type(error).__name__,
                    "msg": str(error),
                    "traceback": tb_str,
                },
            )
