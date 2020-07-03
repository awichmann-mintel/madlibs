import os
from multiprocessing import cpu_count

import environ
from mintel_logging import LogLevel
from mintel_logging.contrib import BaseGunicornLogger

env = environ.Env()

bind = ["0.0.0.0:80"]
workers = (cpu_count() * 2) + 1
accesslog = "-"
errorlog = "-"


class GunicornLogger(BaseGunicornLogger):
    SERVICE = "everest.mad-libz"
    LEVEL = env(
        "MINTEL_LOGGING_LEVEL", default=LogLevel.INFO, cast=LogLevel.__members__.get
    )


LOGGING_CONFIG = "config.gunicorn.GunicornLogger"


for k, v in os.environ.items():
    if k.startswith("GUNICORN_"):
        key = k.split("_", 1)[1].lower()
        locals()[key] = v
