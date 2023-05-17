from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb
import click
import re
from new_user import new_user

from db.models import Base, User, Bike

database_path = "db/spracket.db"

engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()


@click.command()
@click.option(
    "--manufacturer",
    prompt="[What is the manufacturer of the bike?]",
    help="Specify the manufacturer of the bike.",
)
@click.option(
    "--model",
    prompt="[What is the model of the bike?]",
    help="Specify the model of the bike.",
)
@click.option(
    "--year",
    prompt="[What is the year of the bike?]",
    help="Specify the year of the bike.",
)
def register(manufacturer, model, year):
    new_bike = Bike(manufacturer=manufacturer, model=model, year=year)
    session.add(new_bike)
    session.commit()


@click.command()
@click.option(
    "--selection",
    prompt="Welcome to Spracket! Are you a new or existing user?",
    type=click.Choice(["new", "existing"]),
    help="Specify if you are a new or existing user.",
)
def welcome(selection):
    if selection == "new":
        click.echo("We need to set you up with an account.")
        new_user()
    else:
        existing_user()


if __name__ == "__main__":
    welcome()
