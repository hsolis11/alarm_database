from database.connect import BaseConnection
from interface import User, AbstractUsersRepo


class Users(BaseConnection, AbstractUsersRepo):

    def get(self, iduser: int = None, tech_id: str = None):
        sql = None
        values = None
        if iduser:
            sql = "SELECT * FROM users WHERE id = ?"
            values = (iduser,)
        elif tech_id:
            sql = "SELECT * FROM users WHERE tech_id = ?"
            values = (tech_id,)

        with self.conn as conn:
            c = conn.cursor()
            c.execute(sql, values)
            data = c.fetchall()
            if data:
                return User(*data)
            else:
                return None

    def put(self, user: User = None):
        pass

    def update(self, user: User = None):
        pass