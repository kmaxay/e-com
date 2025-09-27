from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.user import UserCreate, UserLogin, UserResponse
import app.database as database
from app.auth import verify_password, create_access_token, SECRET_KEY, ALGORITHM, get_password_hash
from jose import JWTError, jwt
from datetime import timedelta

from sqlalchemy.orm import Session
from app.models.user import User, Base
Base.metadata.create_all(bind=database.engine)

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate,  db: Session = Depends(database.get_db)):
    try:
        # user = database.create_user(user_data)
        db_user = User( 
                       full_name=user_data.full_name, 
                       username=user_data.username, 
                       phone_number=user_data.phone_number, 
                       is_active=True,
                       password=get_password_hash(user_data.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
        return UserResponse(**user.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(login_data: UserLogin):
    user = database.get_user_by_phone(login_data.phone_number)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid phone number or password")
    
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=timedelta(days=7)  # Longer expiry for better UX
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": UserResponse(**user.dict())
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(user_id: int = Depends(get_current_user)):
    user = database.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.dict())