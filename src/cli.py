import click
import yaml
from sys import exit
from cfbulk import log
from cfbulk.replace import replace


@click.command()
@click.option('--dry', default=False, type=bool, help='Simulate run')
@click.option('--config', '-c', type=click.Path(), default='config.yml', help='Config file to use')
def main(dry: bool, config: str):
    """Bulk replace ip addresses in cloudflar dns"""
    config = yaml.load(open(config, 'r'), Loader=yaml.FullLoader)

    if dry is not True:
        if not log.confirm('Doing actual changes via API, continue?'):
            log.error('Cancel')
            exit(-1)

    replace()


if __name__ == '__main__':
    main()
