import database
from app import bcrypt, login_manager
from flask_login import UserMixin
from interface import User
from database import Users


@login_manager.user_loader
def load_user(user_id):
    user = UserManager()
    return user.get(user_id)


class UserManager(UserMixin):
    def __init__(self):
        self.user: User = None
        self._is_active: bool = False
        self._is_authenticated: bool = False
        self._is_anonymous: bool = True

    @property
    def is_active(self):
        return self._is_active

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @property
    def is_anonymous(self):
        return self._is_anonymous

    def get(self, iduser: int = None):
        user = Users().get(iduser=iduser)
        if user:
            self.user = user
            return self

    def get_id(self):
        if self.user:
            return self.user.iduser

    def register(self):
        pass

    def login(self):
        pass