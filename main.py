from fastapi import FastAPI
from users.router import router as user_router

app = FastAPI()
app.include_router(router=user_router)

app.get('/')
def test():
    return {'message': True}