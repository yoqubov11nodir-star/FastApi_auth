from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from users.models import User
from users.schemas import SignUpSchema, LoginSchema
from werkzeug.security import generate_password_hash, check_password_hash

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/sign-up', status_code=status.HTTP_201_CREATED)
def sign_up(user_data: SignUpSchema, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail='Bu username band')
    
   
    db_email = db.query(User).filter(User.email == user_data.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail='Bu email band')
    
    new_user = User(
        username=user_data.username,
        first_name=user_data.first_name,
        email=user_data.email,
        password=generate_password_hash(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User muvaffaqiyatli yaratildi",
        "user": {
            "username": new_user.username,
            "email": new_user.email
        }
    }

@router.post('/login')
def login(user_data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    
    if not check_password_hash(user.password, user_data.password):
        raise HTTPException(status_code=400, detail="Parol noto'g'ri")
    
    return {"message": "Xush kelibsiz!", "username": user.username}