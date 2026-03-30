from repositories.auth_repo import AuthRepo
from models.auth_model import (
    AuthModel, 
    UserAlreadyExistsError, 
    TokenError, 
    InvalidCredentials
)

class AuthController:
    def __init__(self):
        self.auth_repo = AuthRepo()

    def register(self, data: dict):
        try:
            user = self.auth_repo.register_user(data)
            return AuthModel.user_info_success(user)
        except UserAlreadyExistsError as e:
            return AuthModel.user_taken_message(e)

    def login(self, data: dict):
        try:
            user = self.auth_repo.login(data)
            return AuthModel.user_info_success(user)
        except InvalidCredentials as e:
            return AuthModel.invalid_credentials_message(e)

    def me_by_id(self, data):
        try:
            user = self.auth_repo.me_by_id(data)
            if not user:
                return AuthModel.user_not_found_message()
            return AuthModel.user_info_success(user)
        except TokenError as e:
            return AuthModel.token_error_message(e)
        
