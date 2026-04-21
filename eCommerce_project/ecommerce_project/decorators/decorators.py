from functools import wraps
from flask import jsonify, request, g
from services.jwt_manager import JWTManager

def handle_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result, status = func(*args, **kwargs)
            return jsonify(result), status
        except Exception as e:
            return {'error': f'Internal server error: {e}'}, 500
    return wrapper

def validate_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if not data:
            return {'error': 'No JSON data provided'}, 400
        return func(*args, **kwargs)
    return wrapper

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            print("No authorization header")
            return {'error': 'No authorization header'}, 401
        
        try:
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
        except IndexError:
            return {'error': 'Invalid authorization header format'}, 401
        
        try:
            jwt_manager = JWTManager()
            decoded = jwt_manager.decode(token)
            g.token = token
            g.user_data = decoded.get('data', {})
            return func(*args, **kwargs)
        except ValueError as e:
            return {'error': str(e)}, 401
        except Exception as e:
            print("why edwin")
            return {'error': 'Invalid token'}, 401
    return wrapper

def require_fields(*required_fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json() or None
            if not data:
                return {'error': 'No JSON data provided'}, 400
            missing = [field for field in required_fields if field not in data]
            if missing:
                return {
                    'error': 'Missing required fields',
                    'fields': missing
                }, 400
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_roles(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_roles = g.user_data.get('roles', [])
            
            has_permission = any(role in allowed_roles for role in user_roles)
            
            if not has_permission:
                print("Require permissions.")
                return {
                    'error': 'Insufficient permissions',
                    'required_roles': list(allowed_roles)
                }, 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

