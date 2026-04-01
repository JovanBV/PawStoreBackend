from flask import Flask
from services.cache_manager import CacheManager
from services.register_first_entrys import RegisterFirsts
from flask_cors import CORS

from routes.user_routes import create_user_blueprint
from routes.product_routes import create_product_blueprint
from routes.auth_routes import create_auth_blueprint
from routes.sale_routes import create_sales_blueprint

from controllers.user_controller import UserController
from controllers.product_controller import ProductController
from controllers.sales_controller import SalesController
from controllers.auth_controller import AuthController

class API():
    def __init__(self):
        self.app = Flask(__name__)
        self._setup_dependencies()
        self._setup_cors()
        self._register_routes()
        self._initialize_project()

    def _setup_dependencies(self):
        self.user_controller = UserController()
        self.product_controller = ProductController()
        self.sales_controller = SalesController()
        self.auth_controller = AuthController()
        self.cache_manager = CacheManager()
        self.app.url_map.strict_slashes = False

    def _setup_cors(self):
        CORS(self.app, resources={
            r"/*": {
                "origins": ["http://localhost:5000", "http://localhost:5174"],
                "methods": ["GET", "POST","PATCH", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        })

    def _register_routes(self):
        user_bp = create_user_blueprint(self.user_controller, self.cache_manager)
        self.app.register_blueprint(user_bp)
        product_bp = create_product_blueprint(self.product_controller, self.cache_manager)
        self.app.register_blueprint(product_bp)
        auth_bp = create_auth_blueprint(self.auth_controller, self.cache_manager)
        self.app.register_blueprint(auth_bp)
        sales_bp = create_sales_blueprint(self.sales_controller, self.cache_manager)
        self.app.register_blueprint(sales_bp)

    def _initialize_project(self):
        try:
            register_firsts = RegisterFirsts()
            register_firsts.initialize_project()
        except Exception as e:
            print(f"Error initializing project: {e}")

