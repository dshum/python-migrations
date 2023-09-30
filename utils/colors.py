import click


def success(line: str):
    click.secho(line, fg="green")


def info(line: str):
    click.secho(line, fg="blue")


def warn(line: str):
    click.secho(line, fg="orange")


def line(line: str):
    click.secho(line)


def error(e):
    click.secho(e, fg="white", bg="red")
