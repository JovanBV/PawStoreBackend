from sqlalchemy.exc import IntegrityError
from psycopg2.errors import ForeignKeyViolation, UniqueViolation, NotNullViolation, StringDataRightTruncation


# ANSI Colors para consola
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


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
        print(f"{Colors.GREEN}✓ SUCCESS:{Colors.RESET} Operación completada exitosamente")
        return data, 200
    
    @staticmethod
    def general_error_message(error):
        print(f"{Colors.RED}✗ GENERAL ERROR:{Colors.RESET} {str(error)}")
        return {"General sales error": str(error)}, 400

    @staticmethod 
    def cart_not_found_message(error):
        print(f"{Colors.RED}✗ CART NOT FOUND:{Colors.RESET} {error}")
        return {"error": f"Cart not found: {error}"}, 400
    
    @staticmethod
    def key_error_message(error: KeyError):
        missing_key = str(error).strip("'\"")
        print(f"{Colors.RED}✗ KEY ERROR:{Colors.RESET} Falta la clave requerida: {Colors.YELLOW}{missing_key}{Colors.RESET}")
        return {"error": f"Missing key information: {str(error)}"}, 400
    
    @staticmethod
    def validation_error_message(e) -> str:
        print(f"{Colors.RED}✗ VALIDATION ERROR:{Colors.RESET} {e}")
        return {"error": e}, 400
    
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
                error_name = error_type.__name__
                print(f"{Colors.RED}✗ DATABASE INTEGRITY ERROR:{Colors.RESET}")
                print(f"  {Colors.YELLOW}Tipo:{Colors.RESET} {error_name}")
                print(f"  {Colors.YELLOW}Mensaje:{Colors.RESET} {message}")
                print(f"  {Colors.YELLOW}Detalles:{Colors.RESET} {str(e.orig)}")
                return {"error": f"{message}, {e}"}, 400
            
    @staticmethod
    def cart_inactive_message(error):
        print(f"{Colors.YELLOW}⚠ CART INACTIVE:{Colors.RESET} {error}")
        return {"error": f"Cart inactive: {error}"}, 400
    
    @staticmethod
    def cart_dont_belong_message():
        print(f"{Colors.RED}✗ UNAUTHORIZED:{Colors.RESET} El carrito no pertenece a este usuario")
        return {"error": f"Cart doesn't belong to user."}, 400