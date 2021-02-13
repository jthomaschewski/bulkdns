import click


def warn(message: str):
    click.secho(message, nl=False, fg='yellow', bold=True)


def error(message: str):
    click.secho(message, nl=False, fg='red', bold=True)


def info(message: str):
    click.secho(message)


def confirm(message: str) -> bool:
    answer = None
    while answer == None:
        warn(message + ' [yn] ')
        input = click.getchar()
        click.echo()

        if input == 'y':
            answer = True
        elif input == 'n':
            answer = False
        else:
            info('Invalid input, please type "y" for yes, "n" for no')
    return answer
