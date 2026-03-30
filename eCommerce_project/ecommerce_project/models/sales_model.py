from sqlalchemy.exc import IntegrityError
from psycopg2.errors import ForeignKeyViolation, UniqueViolation, NotNullViolation, StringDataRightTruncation


class CartNotBelongToUserError(ValueError):
    pass


class CartInactiveError(ValueError):
    pass

class CartNotFoundError(ValueError):
    pass

class InactiveProducts(ValueError):
    pass

class InsufficientStock(ValueError):
    pass

class SalesModel:
    def __init__(self):
        pass

    @staticmethod
    def success_message(data):
        return data, 200
    
    @staticmethod
    def general_error_message(error):
        return {"General sales error": str(error)}, 400
    @staticmethod 
    def cart_not_found_message(error):
        return {"error": f"Cart not found: {error}"}, 400
    
    @staticmethod
    def key_error_message(error: KeyError):
        return {"error": f"Missing key information: {str(error)}"}, 400
    
    
    @staticmethod
    def handle_integrity_error(e: IntegrityError) -> str:
        errors = {
            UniqueViolation: "Value cannot be duplicated.",
            ForeignKeyViolation: "This relation violates tables restrictions.",
            NotNullViolation: "Required field is missing",
            StringDataRightTruncation: "Value does not fit column restrictions"
        }
        for error_type, message in errors.items():
            if isinstance(e.orig, error_type):
                return {"error": f"{message}, {e}"}, 400
            
    @staticmethod
    def cart_inactive_message(error):
        return {"error": f"Cart inactive: {error}"}, 400
    
    @staticmethod
    def cart_dont_belong_message():
        return {"error": f"Cart doesn't belong to user."}, 400
    
