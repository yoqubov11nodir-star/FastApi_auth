from database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime, Float, ForeignKey
from datetime import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    user_name = Column(String(50), unique=True,index=True)
    first_name = Column(String(50),nullable=True)
    email = Column(String,unique=True,index=True)
    password = Column(String(300))

    is_staff = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())


    def __repr__(self):
        return f"<User {self.user_name}>"
    

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True)
    jti = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String) 
    quantity = Column(Integer, default=1)
    price = Column(Float)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)