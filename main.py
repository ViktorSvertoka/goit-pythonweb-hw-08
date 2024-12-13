from fastapi import FastAPI
from src.api import utils, contacts, birthdays

app = FastAPI()

app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(birthdays.router, prefix="/api")
