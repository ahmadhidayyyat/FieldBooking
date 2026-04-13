from fastapi import FastAPI
from database import engine, Base

import models 


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FieldBooking API",
    description="Microservice backend untuk manajemen pemesanan lapangan.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Selamat datang di API FieldBooking. Server berjalan dengan baik!"}


