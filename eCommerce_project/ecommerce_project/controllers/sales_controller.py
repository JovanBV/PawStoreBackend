from repositories.sales_repo import SalesRepo
from models.sales_model import SalesModel, CartNotFoundError, CartInactiveError, CartNotBelongToUserError
from sqlalchemy.exc import IntegrityError
from services.jwt_manager import JWTManager
from utils.email import send_email

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

    def create_shopping_cart(self, user_id, request_data):
        try:
            items = request_data.get('items')
            if not items:
                return SalesModel.validation_error_message(
                    "At least one item is required to create a cart"
                )
            
            if not request_data.get('id'):
                new_cart = self.sales_repo.insert_shopping_cart(user_id)
                cart_id = new_cart["id"]
            else:
                cart_id = request_data['id']
                self.sales_repo.delete_all_cart_items(cart_id, user_id)
            
            added_items = []
            for item in items:
                item["cart_id"] = cart_id
                result = self.sales_repo.insert_product(item, user_id)
                added_items.append(result["cart_item"])
            
            return SalesModel.success_message({
                "id": cart_id,
                "items": added_items,
                "total_amount": result["cart_total"]
            })
        except CartNotFoundError as e:
            return SalesModel.cart_not_found_message(e)
        except CartInactiveError as e:
            return SalesModel.cart_inactive_message(e)
        except CartNotBelongToUserError as e:
            return SalesModel.cart_dont_belong_message()
        except IntegrityError as e:
            return SalesModel.handle_integrity_error(e)
        except ValueError as e:
            return print("ValueError: ", e)
        except Exception as e:
            print(f"Exception: {e}")
            return SalesModel.general_error_message(e)

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

    def all_process_checkout(self, cart_id, user_id: int):
        try:
            checkout = self.sales_repo.create_checkout(cart_id, user_id)
            return SalesModel.success_message(checkout)
        except CartNotFoundError as e:
            return SalesModel.cart_not_found_message(e)
        except CartInactiveError as e:
            return SalesModel.cart_inactive_message(e)
        except CartNotBelongToUserError as e:
            return SalesModel.cart_dont_belong_message()
        except Exception as e:
            return SalesModel.general_error_message(e)
        
    def get_receipt(self, cart_id, user_id, user_email):
        try:
            receipt = self.sales_repo.get_receipt(cart_id, user_id)
            innactive_cart = self.sales_repo.get_innactive_shopping_cart(cart_id, user_id)
            response = {**receipt, **innactive_cart}
            send_email(user_email, response)
            return SalesModel.success_message(response)
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