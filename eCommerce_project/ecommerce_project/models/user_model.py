from sqlalchemy.exc import IntegrityError, DataError
from psycopg2.errors import ForeignKeyViolation, UniqueViolation, NotNullViolation, StringDataRightTruncation

class UserNotFoundError(ValueError):
    pass

class AddressNotFoundError(ValueError):
    pass

class RoleNotFoundError(ValueError):
    pass

class UserModel:
    def __init__(self):
        pass

    @staticmethod
    def user_not_found_message():
        return {"error": f"ID doesn't match any available user."}, 404

    @staticmethod
    def from_rows_to_dict(data):
        if data is None:
            return None
        result = [{k:v for k,v in item._asdict().items()} for item in data]
        return result
    
    @staticmethod
    def from_single_row_to_dict(data):
        if data is None:
            return None
        result = {k: v for k, v in data._asdict().items()}
        return result
    
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
    def handle_data_error(e: DataError) -> str:
        errors = {
            StringDataRightTruncation: "Value does not meet column restrictions."
        }
        for error_type, message in errors.items():
            if isinstance(e.orig, error_type):
                return {"error": f"{message}, {e}"}, 400
            
    @staticmethod
    def success_message(data, success_message=200):
        return data, success_message

    @staticmethod
    def role_not_found_message():
        return {"error": "Role not found"}, 404
    
    @staticmethod
    def key_error_message(error: KeyError):
        return {"error": f"Missing key information: {str(error)}"}, 400
    
    @staticmethod
    def error_message(e):
        return {"error": f"Error: {e}"}, 404
    
    @staticmethod
    def address_not_found_message(e):
        return {"error": f"Address from user {e} not found."}