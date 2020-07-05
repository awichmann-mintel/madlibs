import os
from multiprocessing import cpu_count

import environ

env = environ.Env()

bind = ["0.0.0.0:80"]
workers = (cpu_count() * 2) + 1
accesslog = "-"
errorlog = "-"


for k, v in os.environ.items():
    if k.startswith("GUNICORN_"):
        key = k.split("_", 1)[1].lower()
        locals()[key] = v
