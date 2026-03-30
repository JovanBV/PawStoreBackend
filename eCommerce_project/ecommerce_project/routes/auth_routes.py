from flask import Blueprint, request, g
from decorators.decorators import handle_request, require_fields, require_auth, require_roles

def create_auth_blueprint(auth_controller, cache_manager):
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('/register', methods=['POST'])
    @handle_request
    @require_fields('email', 'password', 'name')
    def register():
        return auth_controller.register(request.get_json())

    @auth_bp.route('/login', methods=['POST'])
    @handle_request
    @require_fields('email', 'password')
    def login():
        return auth_controller.login(request.get_json())
    
    @auth_bp.route('/me', methods=['GET'])
    @handle_request
    @require_auth
    @require_roles("user", "admin")
    def me():
        return auth_controller.me_by_id(g.user_data)

    return auth_bp