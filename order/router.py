from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth2 import AuthJWT
from database import get_db
from users.models import User, Cart, Order
from users.schemas import OrderResponse, OrderStatusUpdate, CartCreate
from typing import List

order_router = APIRouter(prefix="/order", tags=["Order & Cart"])

def get_current_user(Authorize: AuthJWT, db: Session):
    Authorize.jwt_required()
    username = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.user_name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")
    return user

@order_router.post("/add-to-cart")
def add_to_cart(item: CartCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = get_current_user(Authorize, db)
    
    new_item = Cart(
        user_id=user.id,
        product_name=item.product_name,
        quantity=item.quantity,
        price=item.price
    )
    db.add(new_item)
    db.commit()
    return {"message": "Mahsulot savatchaga qo'shildi"}

@order_router.get("/my-cart")
def view_cart(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = get_current_user(Authorize, db)
    cart_items = db.query(Cart).filter(Cart.user_id == user.id).all()
    return cart_items

@order_router.post("/checkout")
def checkout(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = get_current_user(Authorize, db)
    
    cart_items = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Savatchangiz bo'sh")

    total = sum(item.price * item.quantity for item in cart_items)

    new_order = Order(user_id=user.id, total_price=total, status="pending")
    db.add(new_order)
    
    db.query(Cart).filter(Cart.user_id == user.id).delete()
    db.commit()
    
    return {"message": "Buyurtma qabul qilindi", "order_id": new_order.id, "total": total}

@order_router.get("/my-orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = get_current_user(Authorize, db)
    return db.query(Order).filter(Order.user_id == user.id).all()

@order_router.delete("/cancel/{order_id}")
def cancel_order(order_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = get_current_user(Authorize, db)
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Faqat kutilayotgan buyurtmani bekor qilish mumkin")
    
    db.delete(order)
    db.commit()
    return {"message": "Buyurtma bekor qilindi"}

@order_router.patch("/status/{order_id}")
def update_status(order_id: int, data: OrderStatusUpdate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = get_current_user(Authorize, db)
    if not user.is_staff:
        raise HTTPException(status_code=403, detail="Sizda adminlik ruxsati yo'q")
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    
    order.status = data.status
    db.commit()
    return {"message": "Buyurtma holati yangilandi"}