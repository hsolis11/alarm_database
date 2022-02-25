from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class User:
    iduser: int
    tech_id: str
    f_name: str
    l_name: str
    password: str
    created_at: str


class AbstractUsersRepo(ABC):

    @abstractmethod
    def get(self, iduser: int = None, tech_id: str = None):
        raise NotImplementedError

    @abstractmethod
    def put(self, user: User = None):
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User = None):
        raise NotImplementedError
