from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Vendor:
    idvendor: int
    vendor: str


class AbstractVendorsRepository(ABC):

    @abstractmethod
    def get_list(self):
        raise NotImplementedError


@dataclass
class EqpModel:
    idmodel: int
    model: str


class AbstractEqpModelsRepository(ABC):

    @abstractmethod
    def get_list(self, vendor=None):
        raise NotImplementedError


@dataclass
class EqpModule:
    idmodule: int
    module: str


class AbstractEqpModulesRepository(ABC):

    @abstractmethod
    def get_list(self, model=None):
        raise NotImplementedError
