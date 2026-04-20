from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from users.router import router as user_router
from users.schemas import Settings
from users.models import BlacklistedToken
from database import get_db

from fastapi_jwt_auth2 import AuthJWT

app = FastAPI(
    title="N75 Backend API",
    description="FastAPI orqali Auth, Cart va Order tizimi",
    version="1.0.0"
)

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWT.AuthJWTException)
def authjwt_exception_handler(request, exc):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exc.message
    )

def check_blacklist(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    jti = Authorize.get_raw_jwt()["jti"]

    token = db.query(BlacklistedToken).filter(BlacklistedToken.jti == jti).first()
    if token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token bekor qilingan (logout bo'lingan), iltimos qayta login qiling"
        )

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "API ishlamoqda. /docs manziliga o'ting."}