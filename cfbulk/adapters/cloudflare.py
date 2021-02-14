
import CloudFlare


class CloudFlareAdapter(object):
    """ All Cloudflare API/lib calls (Support other dns providers in the future?) """

    def __init__(self, auth) -> None:
        self.cf = CloudFlare.CloudFlare(token=auth['token'])
        self.cf_raw = CloudFlare.CloudFlare(
            token=auth['token'],
            raw=True
        )

    def zones(self) -> dict:
        zones = []
        page_number = 0
        while True:
            page_number += 1
            raw_results = self.cf_raw.zones.get(
                params={'per_page': 50, 'page': page_number})

            zones_result = raw_results['result']
            for zone in zones_result:
                zones.append({
                    'id': zone['id'],
                    'name': zone['name']
                })
            total_pages = raw_results['result_info']['total_pages']

            if page_number == total_pages:
                break

        return zones

    def records(self, zone_id: str, record_types: list = ['a', 'aaaa', 'cname']) -> list:
        records = []
        page_number = 0
        while True:
            page_number += 1
            raw_results = self.cf_raw.zones.dns_records.get(
                zone_id,
                params={'per_page': 50, 'page': page_number}
            )

            record_result = raw_results['result']
            for record in record_result:
                record_type = record['type'].lower()
                if not record_type in record_types:
                    continue
                records.append({
                    'id': record['id'],
                    'zone_id': zone_id,
                    'type': record_type,
                    'name': record['name'],
                    'content': record['content'],
                    'ttl': record['ttl'],
                })
            total_pages = raw_results['result_info']['total_pages']

            if page_number == total_pages:
                break

        return records

    def update_record(self, zone_id: str, record_id: str, config):
        data = {'content': config['to']}
        if 'ttl' in config:
            data['ttl'] = config['ttl']
        self.cf.zones.dns_records.patch(zone_id, record_id, data=data)
