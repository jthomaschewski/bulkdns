from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    def zones(self) -> dict:
        pass

    @abstractmethod
    def records(self, zone_id: str, record_types: list = ['a', 'aaaa', 'cname']) -> list:
        pass

    @abstractmethod
    def update_record(self, zone_id: str, record_id: str, config):
        pass
