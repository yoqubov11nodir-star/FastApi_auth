from users.models import User
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from users.schemas import SignUpSchema
from sqlalchemy.orm import Session
from database import engine
from werkzeug.security import generate_password_hash, check_password_hash

router = APIRouter(prefix='/auth', tags=['auth'], )

session = Session(bind=engine)

@router.post('/sign-up')
def sign_up(user: SignUpSchema):
    session_username = session.query(User).filter(User.username == user.username).first()
    if session_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bu username band')
    
    session_email = session.query(User).filter(User.email == user.email).first()
    if session_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bu email band')
    
    user = User(
        username = user.username,
        first_name = user.first_name,
        email = user.email,
        password = generate_password_hash(user.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    response = {
        'status': status.HTTP_201_CREATED,
        'message': 'user  yaratildi',
        'data': {
            'username': user.username,
            'first_name': user.first_name,
            'email': user.email,
        }
    }

    return response