from repositories.product_repo import ProductRepo
from models.product_model import ProductNotFoundError, ProductNotCreatedError, ProductModel
from sqlalchemy.exc import IntegrityError

class ProductController:
    def __init__(self):
        self.product_repo = ProductRepo()

    def create_product(self, data: dict):
        try:
            new_product = self.product_repo.insert_product(data)
            return ProductModel.success_message(new_product)
        except ProductNotCreatedError as e:
            return ProductModel.product_not_created_error_message(e)
        except IntegrityError as e:
            return ProductModel.handle_integrity_error(e)
        except KeyError as e:
            return ProductModel.key_error_message(e)
        except Exception as e:
            return ProductModel.general_error_message(e)
    
    def get_product_with_id(self, id: int):
        try:
            product = self.product_repo.get_product_with_id(id)
            return ProductModel.success_message(product)
        except ProductNotFoundError as e:
            return ProductModel.product_not_found_message(e)
        except Exception as e:
            return ProductModel.general_error_message(e)
    
    def delete_product(self, id: int):
        try:
            print("id in delete product: ", id)
            deleted = self.product_repo.soft_delete_product_with_id(id)
            return ProductModel.success_message(deleted)
        except ProductNotCreatedError as e:
            return ProductModel.product_not_found_message(e)
        except ProductNotFoundError as e:
            return ProductModel.product_not_found_message(e)

    def get_all_products(self):
        try:
            all_products = self.product_repo.get_all_products()
            return ProductModel.success_message(all_products)
        except Exception as e:
            return ProductModel.general_error_message(e)

    def update_products_info(self, id: int, data: dict):
        try:
            updated_product = self.product_repo.update_product_stock_with_id(id, data)
            return ProductModel.success_message(updated_product)
        except IntegrityError as e:
            return ProductModel.handle_integrity_error(e)
        except ProductNotFoundError as e:
            return ProductModel.product_not_found_message(e)
        except KeyError as e:
            return ProductModel.key_error_message(e)


