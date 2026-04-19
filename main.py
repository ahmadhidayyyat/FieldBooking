from fastapi import FastAPI
from database import engine, Base

import models 
import routers.user as user_router
import routers.booking as booking_router
import routers.auth as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FieldBooking API",
    description="Microservice backend untuk manajemen pemesanan lapangan.",
    version="1.0.0"
)

app.include_router(user_router.router)
app.include_router(booking_router.router)
app.include_router(auth_router.router)

@app.get("/")
def read_root():
    return {"message": "Selamat datang di API FieldBooking. Server berjalan dengan baik!"}


