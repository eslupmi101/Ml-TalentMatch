import reflex as rx


import os

from dotenv import find_dotenv, load_dotenv
from client.templates import template

import reflex as rx

load_dotenv(find_dotenv())

HOST_WITH_SCHEMA = os.getenv("HOST_WITH_SCHEMA")


config = rx.Config(
    app_name="client",
    api_url=f'{HOST_WITH_SCHEMA}:8000',
)
