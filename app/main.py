from fastapi import Depends, FastAPI

from app.oauth2 import get_current_user
from . import schemas
from .database import engine
from .routers import assistant, user, code, email, event, auth, ticket

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(code.router)
app.include_router(email.router)
app.include_router(event.router)
app.include_router(auth.router)
app.include_router(assistant.router)
app.include_router(ticket.router)


@app.get("/")
def root():
    return {"status": "Server is running..."}
    
