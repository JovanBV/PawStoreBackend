from models.product_model import ProductNotFoundError
from sqlalchemy import select
from services.db_manager import DBManager
from services.models import Products
from datetime import datetime

class ProductRepo(DBManager):
    def __init__(self):
        super().__init__()

    def get_product_with_id(self, id):
        with self.Session() as session:
            product = session.get(Products, id)
            if not product or product.is_deleted:
                raise ProductNotFoundError(id)
            return product.to_dict()

    def insert_product(self, data):
        print("data in insert: ", data)
        with self.Session.begin() as session:
            product = Products(
                name=data['name'],
                stock=data['stock'],
                is_active=data.get('is_active'),
                price=data['price'],
                image_url=data['image_url'],
                category=data['category'],
                description=data['description']
            )
            session.add(product)
            session.flush()
            print("data in insert_product(repo): ", data)

            return product.to_dict()

    def soft_delete_product_with_id(self, id):
        with self.Session.begin() as session:
            product = session.get(Products, id)
            if not product or product.is_deleted:
                raise ProductNotFoundError(id)
            
            product.is_deleted = True
            product.deleted_at = datetime.now()
            return product.to_dict()

    def get_all_products(self):
        with self.Session() as session:
            stmt = select(Products)
            products = session.scalars(stmt).all()
            return [product.to_dict() for product in products if not product.is_deleted]

    def update_product_stock_with_id(self, id, data):
        with self.Session.begin() as session:
            product = session.get(Products, id)
            if not product or product.is_deleted:
                raise ProductNotFoundError(id)
            product.stock = data['stock']
            product.name = data['name']
            product.description = data['description']
            product.price = data['price']
            product.category = data['category']
            product.image_url = data['image_url']
            return product.to_dict()