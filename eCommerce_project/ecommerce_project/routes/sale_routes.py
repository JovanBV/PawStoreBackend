from flask import Blueprint, request, g
from decorators.decorators import handle_request, require_auth, require_fields, require_roles

def create_sales_blueprint(sales_controller, cache_manager):
    sales_bp = Blueprint('sales', __name__)
    @sales_bp.route('/cart/<int:cart_id>', methods=['GET'])
    @handle_request
    @require_auth
    @require_roles("user", "admin")
    def get_cart(cart_id):
        return sales_controller.get_shopping_cart(cart_id, g.user_data['id'])



    @sales_bp.route('/cart', methods=['POST'])
    @handle_request
    @require_auth
    @require_roles("admin", "user")
    def create_cart():
        return sales_controller.create_shopping_cart(g.user_data['id'], request.get_json())
    
    @sales_bp.route('/cart/<int:cart_id>', methods=['DELETE'])
    @handle_request
    @require_auth
    @require_roles("admin", "user")
    def delete_cart(cart_id):
        return sales_controller.delete_shopping_cart(cart_id, g.user_data['id'])

    @sales_bp.route('/cart/all', methods=['GET'])
    @handle_request
    @require_auth
    @require_roles("admin", "user")
    def get_all_carts_from_user():
        return sales_controller.get_all_shopping_carts_from_user(g.user_data['id'])

    @sales_bp.route('/product/add', methods=['POST'])
    @handle_request
    @require_auth
    @require_roles("admin", "user")
    @require_fields("product_id", "amount")
    def create_shopping_cart_product():
        return sales_controller.insert_product_to_cart(request.get_json(), g.user_data['id'])

    @sales_bp.route('/checkout', methods=['POST'])
    @handle_request
    @require_auth
    @require_roles("admin", "user")
    def get_checkout():
        print("id", request.get_json())
        return sales_controller.all_process_checkout(request.get_json(), g.user_data['id'])

    @sales_bp.route('/receipt/<int:id>', methods=['POST'])
    @handle_request
    @require_auth
    @require_roles("admin", "user")
    def get_receipt(id):
        user_email = request.get_json()
        return sales_controller.get_receipt(id, g.user_data['id'], user_email)
    
    @sales_bp.route('/receipt/all', methods=['GET'])
    @handle_request
    @require_auth
    @require_roles("admin", "user")
    def get_all_receipts():
        return sales_controller.get_all_receipts(g.user_data['id'])
    
    return sales_bp