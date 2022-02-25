from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AlarmCard:
    rowid: int
    alarm_id: str
    title: str
    message: str
    cause: str
    response: str


@dataclass
class AlarmDetails(AlarmCard):
    idvendor: int
    vendor: str
    idmodel: int
    model: str
    idmodule: int
    module: str


class AbstractAlarmsDB(ABC):

    @abstractmethod
    def get_detail_list(self, vendor=None, model=None, module=None, alarm_id=None):
        raise NotImplementedError
