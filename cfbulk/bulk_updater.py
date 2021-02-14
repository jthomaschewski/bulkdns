from . import log
from .adapters import CloudFlareAdapter
from .config import config_schema


class BulkUpdater(object):
    def __init__(self, config: object) -> None:
        config_schema.validate(config)
        self.config = config
        self.api = CloudFlareAdapter(config['auth'])

    def replace(self, dry: bool):
        matches = self._find_replace_matches()

        log.info('\n\nList of changes: ')
        for match in matches:
            record = match['record']
            conf = match['config']
            log.info('  %s - %s : from: %s to: %s ' %
                     (record['name'], record['type'], conf['from'], conf['to']))

        if not log.confirm('\n\nExecute changes?'):
            log.warn('Cancelled')
            return

        for match in matches:
            record = match['record']
            conf = match['config']
            exec_info = '%s - %s : from: %s to: %s ' % (
                record['name'], record['type'], conf['from'], conf['to'])

            if dry is True:
                log.debug('...exec (dry): %s ' % exec_info)
            else:
                log.debug('...exec (api): %s ' % exec_info)
                self.api.update_record(match['record']['zone_id'],
                                       match['record']['id'], match['config'])

    def _find_replace_matches(self) -> list:
        zones = self.api.zones()
        domains = list(map(lambda z: z['name'], zones))
        log.debug('found zones: %s' % domains)

        # find records to patch
        replace_config = self.config['replace']
        record_types = replace_config.keys()
        matches = []

        for zone in zones:
            log.debug('...fetching record of %s' % zone['name'])
            records = self.api.records(zone['id'], record_types)
            for record in records:
                match = self._find_record_match(
                    record, replace_config[record['type']])
                if match != None:
                    matches.append(match)

        return matches

    def _find_record_match(self, record, replace_configs):
        for replace_config in replace_configs:
            if replace_config['from'] == record['content']:
                return {'config': replace_config, 'record': record}
        return None
