from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb
import os
import click

from db.models import Base, User, Bike

# Get the current directory path
current_directory = os.path.dirname(os.path.abspath(__file__))

# Build the path to the database file within the "db" directory
database_path = os.path.join(current_directory, "db", "spracket.db")

engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()


@click.command()
@click.option(
    "--action",
    prompt="[Are you here to register or buy?]",
    type=click.Choice(["register", "buy"]),
    help="Specify the action to perform.",
)
def welcome(action):
    click.echo(f"Welcome to Spracket! You chose: {action}")


if __name__ == "__main__":
    welcome()
