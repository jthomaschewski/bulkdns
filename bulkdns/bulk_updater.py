from . import log
from .adapters import ADAPTERS, BaseAdapter
from .config import config_schema


class BulkUpdater(object):
    def __init__(self, config: object) -> None:
        # validate config
        config_schema.validate(config)
        self.config = config
        # initiate concrete api adapter (cloudflare)
        provider_name = config['provider']
        provider_adapter = ADAPTERS[provider_name]
        provider_config = {}
        if provider_name in config['auth']:
            provider_config = config['auth'][provider_name]
        self.api: BaseAdapter = provider_adapter(provider_config)

    def replace(self, dry: bool):
        matches = self._find_replace_matches()

        log.info('\n\nList of changes: ')
        for match in matches:
            zone = match['zone']
            record = match['record']
            conf = match['config']
            log.info(' (%s)  %s - %s : from: %s to: %s ' %
                     (zone['name'], record['name'], record['type'], conf['from'], conf['to']))

        if not log.confirm('\n\nExecute changes?'):
            log.warn('Cancelled')
            return

        for match in matches:
            record = match['zone']
            record = match['record']
            conf = match['config']
            exec_info = '(%s) %s - %s : from: %s to: %s ' % (
                zone['name'], record['name'], record['type'], conf['from'], conf['to'])

            if dry is True:
                log.debug('...exec (dry): %s ' % exec_info)
            else:
                log.debug('...exec (api): %s ' % exec_info)
                self.api.update_record(
                    zone_id=match['zone']['id'],
                    record_id=match['record']['id'],
                    match_config=match['config']
                )

    def _find_replace_matches(self) -> list:
        log.debug('fetching zones...')
        zones = self.api.zones()

        # find records to patch
        replace_config = self.config['replace']
        record_types = replace_config.keys()
        matches = []

        for zone in zones:
            log.debug('fetching records of %s...' % zone['name'])
            records = self.api.records(zone['id'], record_types)
            for record in records:
                match = self._find_record_match(
                    zone,
                    record,
                    replace_config[record['type']],
                )
                if match != None:
                    matches.append(match)

        return matches

    def _find_record_match(self, zone, record, replace_configs):
        for replace_config in replace_configs:
            if replace_config['from'] == record['content']:
                return {'config': replace_config, 'record': record, 'zone': zone}
        return None
