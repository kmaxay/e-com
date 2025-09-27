from sqlalchemy import Column, Boolean, String
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    phone_number = Column(String, nullable=False)
    username = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    password = Column(String, nullable=False)