from repositories.sales_repo import SalesRepo
from models.sales_model import SalesModel, CartNotFoundError, CartInactiveError, CartNotBelongToUserError
from sqlalchemy.exc import IntegrityError
from services.jwt_manager import JWTManager

class SalesController():
    def __init__(self):
        self.sales_repo = SalesRepo()
        self.jwt_manager = JWTManager()

    def get_shopping_cart(self, id: int, user_id):
        try:
            cart = self.sales_repo.get_shopping_cart(id, user_id)
            return SalesModel.success_message(cart)
        except CartNotFoundError as e:
            return SalesModel.cart_not_found_message(e)
        except CartNotBelongToUserError as e:
            return SalesModel.cart_dont_belong_message()
        except Exception as e:
            return SalesModel.general_error_message(e)

    def create_shopping_cart(self, user_id):
        try:
            new_cart = self.sales_repo.insert_shopping_cart(user_id)
            return SalesModel.success_message(new_cart)        
        except IntegrityError as e:
            return SalesModel.handle_integrity_error(e)
        except CartNotFoundError as e:
            return SalesModel.cart_not_found_message()
        except KeyError as e:
            return SalesModel.key_error_message(e)

    def delete_shopping_cart(self, id: int, user_id: int):
        try:
            deleted = self.sales_repo.soft_delete_shopping_cart(id, user_id)
            return SalesModel.success_message(deleted)
        except CartNotFoundError as e:
            return SalesModel.cart_not_found_message(e)
        except CartInactiveError as e:
            return SalesModel.cart_inactive_message(e)
        except CartNotBelongToUserError as e:
            return SalesModel.cart_dont_belong_message()
        except Exception as e:
            return SalesModel.general_error_message(e)
    
    def get_all_shopping_carts_from_user(self, user_id):
        try:
            carts = self.sales_repo.get_all_shopping_carts_from_single_user(user_id)
            return SalesModel.success_message(carts)
        except Exception as e:
            return SalesModel.general_error_message(e)

    def insert_product_to_cart(self, data: dict, user_id: int):
        try:
            data = self.sales_repo.insert_product(data, user_id)
            return SalesModel.success_message(data)
        except CartNotFoundError as e:
            return SalesModel.cart_not_found_message(e)
        except CartInactiveError as e:
            return SalesModel.cart_inactive_message(e)
        except CartNotBelongToUserError as e:
            return SalesModel.cart_dont_belong_message()
        except Exception as e:
            return SalesModel.general_error_message(e)

    def all_process_checkout(self, data: dict, user_id: int):
        try:
            checkout = self.sales_repo.create_checkout(data['cart_id'], user_id)
            return SalesModel.success_message(checkout)
        except CartNotFoundError as e:
            return SalesModel.cart_not_found_message(e)
        except CartInactiveError as e:
            return SalesModel.cart_inactive_message(e)
        except CartNotBelongToUserError as e:
            return SalesModel.cart_dont_belong_message()
        except Exception as e:
            return SalesModel.general_error_message(e)
        
    def get_receipt(self, cart_id, user_id):
        try:
            receipt = self.sales_repo.get_receipt(cart_id, user_id)
            return SalesModel.success_message(receipt)
        except CartNotFoundError as e:
            return SalesModel.cart_not_found_message(e)
        except CartNotBelongToUserError as e:
            return SalesModel.cart_dont_belong_message()
    
    def get_all_receipts(self, user_id):
        try:
            all_receipts = self.sales_repo.get_all_receipts_from_user(user_id)
            return SalesModel.success_message(all_receipts)
        except CartNotFoundError as e:
            return SalesModel.cart_not_found_message(e)
        except CartNotBelongToUserError as e:
            return SalesModel.cart_dont_belong_message()