import logging
import signal
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.controllers import (
    stripe_payments_controller,
)
from src.controllers.middleware.log_middleware import LogMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LogMiddleware)
app.include_router(stripe_payments_controller.router)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def graceful_shutdown(signum, frame) -> None:
    logging.info("Gracefully shutting down the server")
    uvicorn_server.should_exit = True
    uvicorn_server.force_exit = True
    sys.exit(0)


def run_server() -> None:
    global uvicorn_server
    uvicorn_config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=58733,
        log_level="info",
    )
    uvicorn_server = uvicorn.Server(uvicorn_config)
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    logging.info("Starting Uvicorn server")
    uvicorn_server.run()
