from flask import Blueprint, request
from decorators.decorators import handle_request, require_auth, require_roles, require_fields


def create_product_blueprint(product_controller, cache_manager):
    product_bp = Blueprint('products', __name__, url_prefix='/products')


    @product_bp.route('/<int:id>', methods=['GET'])
    @handle_request
    @cache_manager.cache_get_one(key_prefix="products", ttl=400)
    def get_product(id):
        return product_controller.get_product_with_id(id)
    
    @product_bp.route('/', methods=['POST'])
    @handle_request
    @require_auth
    @require_roles("admin")
    @require_fields("name", "description", "stock", "price", "image_url", "category")
    # @cache_manager.invalidate_cache("products:*")
    def create_product():
        return product_controller.create_product(request.get_json())

    @product_bp.route('/<int:id>', methods=['DELETE'])
    @handle_request
    @require_auth
    @require_roles("admin")
    # @cache_manager.invalidate_cache("products:*")
    def delete_product(id):
        print("id in routes: ", id)
        return product_controller.delete_product(id)

    @product_bp.route('/', methods=['GET'])
    @handle_request
    # @cache_manager.cache_get(key_prefix="products", ttl=400)
    def get_all_products():
        return product_controller.get_all_products()

    @product_bp.route('/<int:id>', methods=['PATCH'])
    @handle_request
    @require_auth
    @require_roles("admin")
    @require_fields("stock", "category", "description", "image_url", "name", "price")
    @cache_manager.invalidate_cache("products:*")
    def update_product(id):
        return product_controller.update_products_info(id, request.get_json())
    
    return product_bp
