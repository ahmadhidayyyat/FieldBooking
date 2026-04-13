from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    field_name = Column(String, index=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    
    # Foreign key merujuk ke tabel users
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Referensi balik (Many-to-One) dari Booking ke User
    owner = relationship("User", back_populates="bookings")
