from services.db_manager import DBManager
from models.sales_model import InactiveProducts, InsufficientStock, CartInactiveError, CartNotFoundError, CartNotBelongToUserError
from sqlalchemy import select, func, delete
from datetime import datetime, timezone
from services.models import ShoppingCarts, Products, CartItems
from services.jwt_manager import JWTManager

class SalesRepo(DBManager):
    def __init__(self):
        super().__init__()
        self.jwt_manager = JWTManager()

    def delete_all_cart_items(self, cart_id, user_id):
        with self.Session.begin() as session:
            cart = self._get_cart_by_id(session, cart_id, user_id)
            stmt = delete(CartItems).where(CartItems.shopping_cart_id == cart.id)
            session.execute(stmt)
            cart.total_amount = 0
            session.flush()

    def get_shopping_cart(self, id, user_id):
        with self.Session() as session:
            cart = self._get_cart_by_id(session, id, user_id)
            stmt = select(CartItems).where(CartItems.shopping_cart_id == cart.id)
            cart_items = session.scalars(stmt).all()

            if cart.is_deleted:
                raise CartNotFoundError
            
            return {
                "id": cart.id,
                "total_amount": cart.total_amount,
                "items": [item.to_dict() for item in cart_items] if cart_items else []
            }

    def get_receipt(self, receipt_id, user_id):
        with self.Session() as session:
            receipt = session.get(ShoppingCarts, receipt_id)
            if receipt.user_id != user_id:
                raise CartNotBelongToUserError(receipt_id)
            if not receipt:
                raise CartNotFoundError(receipt_id)
            if receipt.is_deleted:
                raise CartNotFoundError(receipt_id)
            if receipt.is_active:
                return {"error": f"cart with id: {receipt_id} has not been checked out yet."}
            return receipt.to_dict()

    def get_all_receipts_from_user(self, user_id):
        all = self.get_all_shopping_carts_from_single_user(user_id)
        all_receipts = [item for item in all if item['is_active'] == False]
        return all_receipts

    def insert_shopping_cart(self, user_id):
        with self.Session.begin() as session:
            new_cart = ShoppingCarts(user_id=user_id)
            session.add(new_cart)
            session.flush()
            return new_cart.to_dict()

    def soft_delete_shopping_cart(self, id, user_id):
        with self.Session.begin() as session:
            cart = self._get_cart_by_id(session, id, user_id)

            cart.is_deleted = True
            cart.is_active = True
            cart.deletion_date = datetime.now(timezone.utc)
            return cart.to_dict()

    def get_all_shopping_carts_from_single_user(self, user_id):
        with self.Session() as session:
            stmt = select(ShoppingCarts).where(ShoppingCarts.user_id == user_id)
            carts = session.scalars(stmt).all()
            return [cart.to_dict() for cart in carts if not cart.is_deleted]

    def get_innactive_shopping_cart(self, id, user_id):
        with self.Session() as session:
            cart = self._get_innactive_cart(session, id, user_id)
            stmt = select(CartItems).where(CartItems.shopping_cart_id == cart.id)
            cart_items = session.scalars(stmt).all()

            if cart.is_deleted:
                raise CartNotFoundError
            
            response = {
                "id": cart.id,
                "total_amount": cart.total_amount,
                "items": []
            }

            for item in cart_items:
                stmt_product = select(Products).where(Products.id == item.product_id)
                product = session.scalars(stmt_product).first()
                
                item_dict = item.to_dict()
                item_dict["name"] = product.name if product else None
                response["items"].append(item_dict)

            return response

    def _get_innactive_cart(self, session, cart_id, user_id):
        cart = session.get(ShoppingCarts, cart_id)
        if not cart:
            raise CartNotFoundError(cart_id)
        if cart.user_id != user_id:
            raise CartNotBelongToUserError(cart_id)
        if cart.is_deleted:
            raise CartNotFoundError("Cart already deleted")

        return cart

    def _get_product(self, session, product_id):
        product = session.get(Products, product_id)
        if not product:
            raise ValueError("Product not found")
        return product
    
    def _validate_product_active(self, product):
        if not product.is_active:
            raise InactiveProducts(f"Product {product.name} is inactive")
    
    def _validate_stock(self, product, amount):
        if product.stock < amount:
            raise InsufficientStock(
                f"Insufficient stock for {product.name}. Available: {product.stock}"
            )
    
    def _get_cart_by_id(self, session, cart_id, user_id):
        cart = session.get(ShoppingCarts, cart_id)
        if not cart:
            raise CartNotFoundError(cart_id)
        if cart.user_id != user_id:
            raise CartNotBelongToUserError(cart_id)
        if not cart.is_active:
            raise CartInactiveError(f"Cart {cart_id} is not active")
        if cart.is_deleted:
            raise CartNotFoundError("Cart already deleted")

        return cart
    
    def _get_or_create_active_cart(self, session, user_id):
        stmt = (
            select(ShoppingCarts).where(
                ShoppingCarts.user_id == user_id,
                ShoppingCarts.is_active == True,
                ShoppingCarts.is_deleted == False
            )
            .order_by(ShoppingCarts.created_at.desc())
        )
        cart = session.scalars(stmt).first()
        if not cart:
            cart = ShoppingCarts(user_id=user_id)
            session.add(cart)
            session.flush()
        return cart
    
    def _get_existing_cart_item(self, session, cart_id, product_id):
        stmt = select(CartItems).where(
            CartItems.shopping_cart_id == cart_id,
            CartItems.product_id == product_id
        )
        return session.scalars(stmt).first()
    
    def _update_cart_item_amount(self, cart_item, additional_amount, product):
        new_amount = cart_item.amount + additional_amount
        
        if product.stock < new_amount:
            raise InsufficientStock(
                f"Insufficient stock for {product.name}. "
                f"Available: {product.stock}, "
                f"Current in cart: {cart_item.amount}, "
                f"Requested: {additional_amount}"
            )
        
        cart_item.amount = new_amount
        return cart_item
    
    def _create_cart_item(self, session, cart_id, product_id, amount, price):
        new_item = CartItems(
            shopping_cart_id=cart_id,
            product_id=product_id,
            amount=amount,
            price=price
        )
        session.add(new_item)
        session.flush()
        return new_item
    
    def _update_cart_total(self, session, cart):
        stmt = select(func.sum(CartItems.amount * CartItems.price)).where(
            CartItems.shopping_cart_id == cart.id
        )
        cart.total_amount = session.scalar(stmt) or 0
    
    def _get_cart_items(self, session, cart_id):
        stmt = select(CartItems).where(CartItems.shopping_cart_id == cart_id)
        return session.scalars(stmt).all()
    
    def _validate_cart_for_checkout(self, cart):
        if not cart.is_active:
            raise CartInactiveError(f"Cart {cart.id} is not active")
        if cart.is_deleted:
            raise CartInactiveError(f"Cart {cart.id} is deleted")
    
    def _validate_items_stock(self, session, items):
        for item in items:
            product = session.get(Products, item.product_id)
            if product.stock < item.amount:
                raise InsufficientStock(f"Insufficient stock for {product.name}")
    
    def _reduce_product_stock(self, session, items):
        for item in items:
            product = session.get(Products, item.product_id)
            product.stock -= item.amount
    
    def _calculate_cart_total(self, items):
        return sum(item.amount * item.price for item in items)
    
    def insert_product(self, data, user_id):
        with self.Session.begin() as session:
            product = self._get_product(session, data["id"])
            self._validate_product_active(product)
            self._validate_stock(product, data["amount"])

            if "cart_id" in data:
                cart = self._get_cart_by_id(session, data["cart_id"], user_id)
            else:
                cart = self._get_or_create_active_cart(session, user_id)
            
            existing_item = self._get_existing_cart_item(
                session, cart.id, data["id"]
            )
            
            if existing_item:
                cart_item = self._update_cart_item_amount(
                    existing_item, data["amount"], product
                )
            else:
                cart_item = self._create_cart_item(
                    session, cart.id, data["id"], 
                    data["amount"], product.price
                )
            
            self._update_cart_total(session, cart)
            session.refresh(cart_item)
            
            return {
                "cart_id": cart.id,
                "cart_item": cart_item.to_dict(),
                "cart_total": cart.total_amount
            }
        
    def create_checkout(self, cart_id, user_id):
        with self.Session.begin() as session:
            cart = self._get_cart_by_id(session, cart_id, user_id)
            self._validate_cart_for_checkout(cart)

            items = self._get_cart_items(session, cart.id)
            if not items:
                print("Error because of empty cart")
                raise ValueError("Cannot checkout an empty cart")
            self._validate_items_stock(session, items)
            self._reduce_product_stock(session, items)

            cart.total_amount = self._calculate_cart_total(items)
            cart.is_active = False
            cart.completed_at = datetime.now(timezone.utc)

            return {
                "cart_id": cart.id,
                "total_amount": cart.total_amount,
                "items": [item.to_dict() for item in items],
                "completed_at": cart.completed_at.isoformat()
            }