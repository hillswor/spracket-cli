import click
from register import register
import ipdb


@click.command()
@click.option(
    "--action",
    prompt="Would you like to register a new bike, remove a previously registered bike, or search the database?",
    type=click.Choice(["register", "remove", "search"]),
    help="Specify if you would like to register a new bike, remove a previously registered bike, or search the database.",
)
def menu(username, action):
    ipdb.set_trace()
