from sqlalchemy import select
from services.db_manager import DBManager
from services.models import Roles, Users, UsersRoles
from repositories.user_repo import UserRepo
import bcrypt

import os
from dotenv import load_dotenv

load_dotenv()

class RegisterFirsts(DBManager):
    def __init__(self):
        super().__init__()
        self.user_repo = UserRepo()
        self.admin_credentials = {
            "email": os.getenv('ADMIN_EMAIL'),
            "name": os.getenv('ADMIN_NAME'),
            "password": os.getenv('ADMIN_PASSWORD')
        }
    
    def initialize_project(self):
        self._create_roles()
        admin_user_id = self._create_admin_user()
        if admin_user_id:
            self._assign_admin_role(admin_user_id)
        
    def _create_roles(self):
        with self.Session.begin() as session:
            user_role = session.scalar(
                select(Roles).where(Roles.role == "user")
            )
            admin_role = session.scalar(
                select(Roles).where(Roles.role == "admin")
            )
            
            if not user_role:
                self.user_repo.insert_user_role({
                    "role": "user",
                    "description": "Basic access"
                })
            
            if not admin_role:
                self.user_repo.insert_user_role({
                    "role": "admin",
                    "description": "Complete access"
                })
    
    def _create_admin_user(self):
        existing_admin = self.user_repo.get_user_by_email(self.admin_credentials['email'])
        
        if existing_admin:
            return existing_admin.id
        
        password_bytes = self.admin_credentials['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        
        admin_data = {
            "email": self.admin_credentials['email'],
            "name": self.admin_credentials['name'],
            "password": hashed_password,
            "phone": None
        }
        
        new_admin = self.user_repo.insert_user(admin_data)
        return new_admin.id
    
    def _assign_admin_role(self, user_id):
        with self.Session.begin() as session:
            admin_role = session.scalar(
                select(Roles).where(Roles.role == "admin")
            )
            
            if not admin_role:
                return
            
            has_admin_role = session.scalar(
                select(UsersRoles).where(
                    UsersRoles.user_id == user_id,
                    UsersRoles.role_id == admin_role.id
                )
            )
            
            if not has_admin_role:
                self.user_repo.insert_role_assignment({
                    "user_id": user_id,
                    "role_id": admin_role.id
                })