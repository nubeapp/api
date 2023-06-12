from fastapi import FastAPI

from app.logger import get_custom_logger

from . import schemas
from .database import engine
from .routers import user, code, email, event, auth, ticket, organization, order

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI(encoding='utf-8')


app.include_router(user.router)
app.include_router(code.router)
app.include_router(email.router)
app.include_router(event.router)
app.include_router(auth.router)
app.include_router(ticket.router)
app.include_router(organization.router)
app.include_router(order.router)


@app.get("/")
def root():
    return {"status": "Server is running..."}


