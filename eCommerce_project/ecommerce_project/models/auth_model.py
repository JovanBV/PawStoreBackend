import functools
from flask import request, jsonify
from services.jwt_manager import JWTManager

jwt_manager = JWTManager()


def allowed_roles(allowed_roles):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            try:
                if not token:
                    return AuthModel.token_error_message("Missing token.")
                
                test = token.replace("Bearer ","")
                user = jwt_manager.decode(test)

                user_roles = user["data"]["roles"]
                for role in user_roles:
                    if role in allowed_roles:
                        return func(*args, **kwargs)
                else:
                    return AuthModel.role_needed_message(role)
            except Exception as e:
                return AuthModel.token_error_message("Token values are not valid.")
        return wrapper
    return decorator

class TokenError(ValueError):
    pass

class RequiredInfoMissingError(ValueError):
    pass

class UserAlreadyExistsError(ValueError):
    pass

class InvalidCredentials(ValueError):
    pass

class TokenError(ValueError):
    pass

class AuthModel:
    
    @staticmethod
    def required_info_missing_message(error):
        return {"error": f"Required info missing: {error}"}, 400

    @staticmethod
    def user_taken_message(error):
        return {"error": f"User already exists: {error}"}, 409
    
    @staticmethod
    def retrieve_token_success(token):
        return {"token": token}, 200

    @staticmethod 
    def token_error_message(error):
        return {"error": f"Error with token: {error}"}, 401

    @staticmethod 
    def invalid_credentials_message(error):
        return {"error": f"Invalid credentials: {error}"}, 401
    
    @staticmethod 
    def role_needed_message(error):
        return {"error": f"Invalid role, to access."}, 403
    
    @staticmethod
    def user_info_success(data):
        return data, 200
