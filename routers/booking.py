from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models.booking as booking_model
import schemas.booking as booking_schema
import models.user as user_model
from auth.jwt import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.post("/", response_model=booking_schema.BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: booking_schema.BookingCreate, current_user: user_model.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_booking = booking_model.Booking(
        field_name=booking.field_name,
        start_time=booking.start_time,
        end_time=booking.end_time,
        owner_id=current_user.id
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return new_booking

@router.get("/", response_model=List[booking_schema.BookingResponse], status_code=status.HTTP_200_OK)
def read_all_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = db.query(booking_model.Booking).offset(skip).limit(limit).all()
    return bookings

@router.get("/{booking_id}", response_model=booking_schema.BookingResponse, status_code=status.HTTP_200_OK)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(booking_model.Booking).filter(booking_model.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking tidak ditemukan")
    return booking

@router.put("/{booking_id}", response_model=booking_schema.BookingResponse, status_code=status.HTTP_200_OK)
def update_booking(booking_id: int, booking_update: booking_schema.BookingCreate, current_user: user_model.User = Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(booking_model.Booking).filter(booking_model.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking tidak ditemukan")
    
    if booking.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this booking")
    
    booking.field_name = booking_update.field_name
    booking.start_time = booking_update.start_time
    booking.end_time = booking_update.end_time
    
    db.commit()
    db.refresh(booking)
    return booking

@router.delete("/{booking_id}", status_code=status.HTTP_200_OK)
def delete_booking(booking_id: int, current_user: user_model.User = Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(booking_model.Booking).filter(booking_model.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking tidak ditemukan")
    
    if booking.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this booking")
    
    db.delete(booking)
    db.commit()
    return {"detail": "Booking berhasil dihapus"}
