
from .base_adapter import BaseAdapter


class DummyAdapter(BaseAdapter):
    """ Just some fake api responses """

    def __init__(self, auth) -> None:
        pass

    def zones(self) -> dict:
        zones = [
            {'id': 'zone1', 'name': 'example.com'},
            {'id': 'zone2', 'name': 'example.org'},
        ]
        return zones

    def records(self, zone_id: str, record_types: list = ['a', 'aaaa', 'cname']) -> list:
        records = [
            {
                'id': 'record1',
                'name': 'recname1',
                'type': 'a',
                'content': '127.0.0.1',
                'ttl': 300
            },
            {
                'id': 'record2',
                'name': 'recname2',
                'type': 'cname',
                'content': 'old.cname.example.com',
                'ttl': 600
            },
        ]

        return records

    def update_record(self, zone_id: str, record_id: str, match_config):
        pass
