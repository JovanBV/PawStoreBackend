from repositories.user_repo import UserRepo
from models.user_model import UserModel, UserNotFoundError, RoleNotFoundError, AddressNotFoundError
from sqlalchemy.exc import IntegrityError, DataError
class UserController:
    def __init__(self):
        self.user_repo = UserRepo()

    def get_user_with_id(self, id: int):
        try:
            user_data = self.user_repo.get_user_with_id(id)
            return UserModel.success_message(user_data.to_dict())
        except UserNotFoundError as e:
            return UserModel.user_not_found_message()

    def delete_user(self, id: int):
        try:
            deleted = self.user_repo.delete_user_with_id(id)
            print(deleted)
            return UserModel.success_message(deleted)
        except UserNotFoundError:
            return UserModel.user_not_found_message()

    def update_user(self, id: int, data: dict):
        try:
            updated = self.user_repo.update_user_name_with_id(id, data)
            return UserModel.success_message(updated)
        except UserNotFoundError:
            return UserModel.user_not_found_message()
        except KeyError as e:
            return UserModel.key_error_message(e)

    def create_role(self, data: dict):
        try:
            new_role = self.user_repo.insert_user_role(data)
            return UserModel.success_message(new_role)
        except IntegrityError as e:
            return UserModel.handle_integrity_error(e)
        except DataError as e:
            return UserModel.handle_data_error(e)
        except KeyError as e:
            return UserModel.key_error_message(e)

    def get_role_with_id(self, id: int):
        try:
            role = self.user_repo.get_role_with_id(id)
            return UserModel.success_message(role)
        except RoleNotFoundError as e:
            return UserModel.role_not_found_message()

    def assign_role_to_user(self, data: dict):
        try:
            assignment = self.user_repo.insert_role_assignment(data)
            return UserModel.success_message(assignment)
        except IntegrityError as e:
            return UserModel.handle_integrity_error(e)

    def create_user_address(self, data: dict, user_id):
        try:
            address = self.user_repo.insert_user_address(data, user_id)
            return UserModel.success_message(address)
        except KeyError:
            return UserModel.key_error_message(e)
        except IntegrityError as e:
            return UserModel.handle_integrity_error(e)

    def get_users(self):
        try:
            users = self.user_repo.get_all_users()
            return UserModel.success_message(users)
        except Exception as e:
            return UserModel.error_message(e)
        
    def get_all_roles(self):
        try:
            all_roles = self.user_repo.get_all_roles()
            return UserModel.success_message(all_roles)
        except Exception as e:
            return UserModel.error_message(e)
        
    def get_all_addresses(self):
        try:
            all = self.user_repo.get_all_addresses()
            return UserModel.success_message(all)
        except Exception as e:
            return UserModel.error_message(e)
    
    def get_all_addresses_from_user(self, user_id: int):
        try:
            all = self.user_repo.get_all_addresses_from_user(user_id)
            return UserModel.success_message(all)
        except AddressNotFoundError as e:
            return UserModel.address_not_found_message(e)
        except Exception as e:
            return UserModel.error_message(e)