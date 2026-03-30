from flask import Blueprint, request, g
from decorators.decorators import handle_request, validate_json, require_roles, require_auth


def create_user_blueprint(user_controller, cache_manager):
    user_bp = Blueprint('users', __name__, url_prefix='/users')

    @user_bp.route('/roles/assignments', methods=['POST'])
    @validate_json
    @handle_request
    @require_auth
    @require_roles("admin")
    def assign_role():
        return user_controller.assign_role_to_user(request.get_json())

    @user_bp.route('/roles', methods=['POST'])
    @validate_json
    @handle_request
    @require_auth
    @require_roles("admin")
    def create_role():
        return user_controller.create_role(request.get_json())

    @user_bp.route('/roles', methods=['GET'])
    @handle_request
    @require_auth
    @require_roles("admin")
    def get_all_roles():
        return user_controller.get_all_roles()

    @user_bp.route('/roles/<int:id>', methods=['GET'])
    @handle_request
    @require_auth
    @require_roles("admin")
    def get_role(id):
        return user_controller.get_role_with_id(id)

    # ============ RUTAS DE DIRECCIONES ============
    @user_bp.route('/addresses/all', methods=['GET'])
    @validate_json
    @handle_request
    @require_auth
    @require_roles("admin")
    def get_address_all_addresses():
        return user_controller.get_all_addresses()

    @user_bp.route('/addresses', methods=['POST'])
    @validate_json
    @handle_request
    @require_auth
    @require_roles("user")
    def create_address():
        return user_controller.create_user_address(request.get_json(), g.user_data['user_id'])

    @user_bp.route('/addresses', methods=['GET'])
    @validate_json
    @handle_request
    @require_auth
    @require_roles("user", "admin")
    def get_all_addresses_from_user():
        return user_controller.get_all_addresses_from_user(g.user_data['id'])

    # ============ RUTAS DE USUARIOS (GENÉRICAS ÚLTIMO) ============
    @user_bp.route('/', methods=['GET'])
    @handle_request
    @require_auth
    @require_roles("admin")
    def get_all_users():
        return user_controller.get_users()

    @user_bp.route('/<int:id>', methods=['GET'])
    @handle_request
    @require_auth
    @require_roles("admin", "user")
    def get_user(id):
        return user_controller.get_user_with_id(id)

    @user_bp.route('/<int:id>', methods=['PATCH'])
    @validate_json
    @handle_request
    @require_auth
    @require_roles("admin")
    def update_user(id):
        return user_controller.update_user(id, request.get_json())

    @user_bp.route('/<int:id>', methods=['DELETE'])
    @handle_request
    @require_auth
    @require_roles("admin")
    def delete_user(id):
        return user_controller.delete_user(id)

    return user_bp