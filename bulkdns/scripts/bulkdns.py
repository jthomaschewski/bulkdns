import click
import yaml
from CloudFlare import cloudflare
from schema import SchemaError

from bulkdns import BulkUpdater, log


@click.command()
@click.option('--dry', flag_value=True, help='Simulate run')
@click.option('--config', '-c', type=click.Path(), default='config.yml', help='Config file to use')
def cli(dry: bool, config: str):
    """Bulk replace ip addresses in cloudflar dns"""

    file = open(config, 'r')
    parsed_config = yaml.load(file, Loader=yaml.FullLoader)
    file.close()

    try:
        bulk = BulkUpdater(parsed_config)
    except SchemaError as err:
        log.error('Invalid config: %s' % err)
        exit(-1)

    if dry is not True:
        if not log.confirm('Doing actual changes via API, continue?'):
            log.error('Cancel')
            exit(-1)

    try:
        bulk.replace(dry)
    except cloudflare.CloudFlareAPIError as err:
        log.error('API error: %d %s' % (err, err))
