import sqlite3
import os

DATABASE = os.path.join('database/test.db')


def get_connection():
    return sqlite3.connect(DATABASE)


class StoreException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors


class BaseConnection:
    def __init__(self):
        try:
            self.conn = get_connection()
        except Exception as e:
            raise StoreException(*e.args, **e.kwargs)
        self._complete = False

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    def complete(self):
        self._complete = True

    def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise StoreException(*e.args)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise StoreException(*e.args)