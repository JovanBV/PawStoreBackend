from sqlalchemy import select, update
from services.db_manager import DBManager
from models.user_model import UserNotFoundError, RoleNotFoundError, AddressNotFoundError
from services.models import Users, Roles, UsersRoles, Addresses

class UserRepo(DBManager):
    def __init__(self):
        super().__init__()

    def delete_user_with_id(self, id):
        with self.Session.begin() as session:
            user = session.get(Users, id)
            if not user or user.is_deleted:
                raise UserNotFoundError(id)
            user.is_deleted = True
            return user.to_dict()

    def update_user_name_with_id(self, id, data):
        with self.Session.begin() as session:
            user = session.get(Users, id)
            if not user or user.is_deleted:
                raise UserNotFoundError
            user.name = data["name"]
            return user.to_dict()

    def insert_user(self, data: dict):
        with self.Session.begin() as session:
            new_user = Users(**data)
            session.add(new_user)
            session.flush()
            user_role = session.query(Roles).filter(Roles.role == "user").first()
            if user_role:
                user_role_assignment = UsersRoles(
                    user_id=new_user.id,
                    role_id=user_role.id
                )
                session.add(user_role_assignment)
            
            session.flush()
            session.refresh(new_user)
            
            _ = new_user.users_roles
            session.expunge(new_user)
            return new_user
    
    def insert_user_role(self, data: dict):
        with self.Session.begin() as session:
            new_role = Roles(**data)
            session.add(new_role)
            session.flush()
            return new_role.to_dict()

    def get_role_with_id(self, id):
        with self.Session() as session:
            role = session.get(Roles, id)
            if not role:
                raise RoleNotFoundError
            return role.to_dict()

    def insert_role_assignment(self, data: dict):
        with self.Session.begin() as session:
            new_assignment = UsersRoles(
                user_id = data['user_id'],
                role_id = data['role_id']
            )
            session.add(new_assignment)
            session.flush()
            return new_assignment.to_dict()

    def insert_user_address(self, data, user_id):
        with self.Session.begin() as session:
            self._unset_default_addresses(session, user_id)
            new_address = Addresses(
                user_id= user_id,
                street_address= data["street_address"],
                country= data["country"],
                city= data["city"],
                postal_code= data["postal_code"],
                is_default= data.get("is_default", True)
            )
            session.add(new_address)
            session.flush()
            return new_address.to_dict()
        
    def get_all_addresses(self):
        with self.Session() as session:
            stmt = select(Addresses)
            all = session.scalars(stmt).all()
            return [a.to_dict() for a in all]

    def _unset_default_addresses(self, session, user_id):
        stmt = (
            update(Addresses)
            .where(
                Addresses.user_id == user_id,
                Addresses.is_default == True
            )
            .values(is_default=False)
        )
        session.execute(stmt)

    def get_users_roles(self, user_id):
        with self.Session() as session:
            roles = session.get(Users, user_id).users_roles
            if not roles:
                raise UserNotFoundError
            return roles.to_dict()

    def get_all_users(self):
        with self.Session() as session:
            stmt = select(Users)
            users = session.scalars(stmt).all()
            return [user.to_dict() for user in users if not user.is_deleted]

    def get_user_by_email(self, email: str):
        with self.Session() as session:
            stmt = select(Users).where(Users.email == email)
            user = session.scalar(stmt)
            if not user or user.is_deleted:
                return None 
            user.get_roles()
            return user

    def get_user_with_id(self, id):
        with self.Session() as session:
            user = session.get(Users, id)
            if not user or user.is_deleted:
                raise UserNotFoundError(id)
            user.get_roles()
            return user
        
    def get_all_roles(self):
        with self.Session() as session:
            stmt = select(Roles)
            roles = session.scalars(stmt).all()
            return [role.to_dict() for role in roles]
        
    def get_all_addresses_from_user(self, user_id):
        with self.Session() as session:
            stmt = select(Addresses).where(Addresses.user_id == user_id)
            all = session.scalars(stmt).all()
            if not all:
                raise AddressNotFoundError(user_id)
            return [a.to_dict() for a in all]