from fastapi import FastAPI
from .database import Base, engine
from .routers import contacts


app = FastAPI(title="Contacts API", version="1.0.0")



Base.metadata.create_all(bind=engine)


app.include_router(contacts.router)

