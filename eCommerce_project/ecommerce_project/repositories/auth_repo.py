from services.jwt_manager import JWTManager
import bcrypt
from models.auth_model import UserAlreadyExistsError, InvalidCredentials
from repositories.user_repo import UserRepo
from sqlalchemy.exc import IntegrityError

class AuthRepo():
    def __init__(self):
        self.jwt_manager = JWTManager()
        self.user_repo = UserRepo()


    def register_user(self, data: dict):
        try:
            data['password'] = self._hash_password(data['password'])
            new_user = self.user_repo.insert_user(data)
            user = self.user_repo.get_user_with_id(new_user.id)
            token, payload = self._generate_token(user)
            return {"token": token, "payload": payload}
        except IntegrityError:
            raise UserAlreadyExistsError(data.get('email', 'unknown'))

    def login(self, data: dict):
        email = data['email']
        password = data['password']
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise InvalidCredentials()
        if not self._verify_password(password, user.password):
            raise InvalidCredentials()
        token, payload = self._generate_token(user)

        return {"token":token, "payload":payload}


    def me_by_id(self, data):
        user = self.user_repo.get_user_with_id(data['id'])
        return user.to_dict()

    def _hash_password(self, password):
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed.decode('utf-8')

    def _generate_token(self, user):
        payload = user.to_dict()
        token = self.jwt_manager.encode(user.to_dict())
        return token, payload

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )