from psycopg2.errors import ForeignKeyViolation, UniqueViolation, NotNullViolation, StringDataRightTruncation
from sqlalchemy.exc import IntegrityError, DataError

class ProductNotFoundError(ValueError):
    pass

class ProductNotCreatedError(ValueError):
    pass

class ProductModel:
    def __init__(self):
        pass

    @staticmethod
    def from_rows_to_dict(data):
        if data is None:
            return None
        result = [{k:v for k,v in item._asdict().items()} for item in data]
        return result

    @staticmethod
    def product_not_found_message(id):
        return {"Product not found": f"ID: {id}"}, 404
    
    @staticmethod
    def product_already_exists_error_message():
        return {"Product error": "Product already exists"}, 409

    @staticmethod
    def success_message(data):
        return data, 200
    
    @staticmethod 
    def product_not_created_error_message(error):
        return {"Product error": str(error)}, 400

    @staticmethod
    def general_error_message(error):
        return {"Product error": f"{error}"}, 404
    
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
    def key_error_message(error: KeyError):
        return {"error": f"Missing key information: {str(error)}"}, 400