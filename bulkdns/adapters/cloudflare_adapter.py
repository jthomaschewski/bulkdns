
import CloudFlare
from bulkdns.errors import BulkDnsApiError
from CloudFlare.exceptions import CloudFlareAPIError, CloudFlareError

from .base_adapter import BaseAdapter
from .ratelimit import Ratelimiter


class CloudFlareAdapter(BaseAdapter):
    """ All Cloudflare API/lib calls (Support other dns providers in the future?) """
    class _catch_cf_error(object):
        def __init__(self, func) -> None:
            self.func = func

        def __call__(self, *args, **kwargs):
            try:
                return self.func(*args, **kwargs)
            except CloudFlareError as err:
                if isinstance(err, CloudFlareAPIError):
                    raise BulkDnsApiError(str(err), int(err), err.error_chain)
                raise

    ratelimit = Ratelimiter(limit=1200, period=300)

    def __init__(self, auth) -> None:
        self.cf = CloudFlare.CloudFlare(**auth)
        self.cf_raw = CloudFlare.CloudFlare(raw=True, **auth)

    @ratelimit
    @_catch_cf_error
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
                    'name': zone['name'],
                })
            total_pages = raw_results['result_info']['total_pages']

            if page_number == total_pages:
                break

        return zones

    @ratelimit
    @_catch_cf_error
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

    @ratelimit
    @_catch_cf_error
    def update_record(self, zone_id: str, record_id: str, match_config):
        data = {'content': match_config['to']}
        if 'ttl' in match_config:
            data['ttl'] = match_config['ttl']
        self.cf.zones.dns_records.patch(zone_id, record_id, data=data)
