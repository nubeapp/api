from fastapi import FastAPI

from app.schemas import user, code, organization, event, ticket, ticket_status_history, order

from .database import engine
from app.api.endpoints import favourite_router, user_router, code_router, email_router, event_router, auth_router, ticket_router, organization_router, order_router, validation_router, ticket_status_history_router

user.Base.metadata.create_all(bind=engine)

app = FastAPI(encoding='utf-8')

app.include_router(user_router.router)
app.include_router(code_router.router)
app.include_router(email_router.router)
app.include_router(event_router.router)
app.include_router(auth_router.router)
app.include_router(ticket_router.router)
app.include_router(organization_router.router)
app.include_router(order_router.router)
app.include_router(favourite_router.router)
app.include_router(validation_router.router)
app.include_router(ticket_status_history_router.router)


@app.get("/")
def root():
    return {"status": "Server is running..."}


