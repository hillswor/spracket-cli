from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb
import click
import re

from db.models import Base, User, Bike

database_path = "db/spracket.db"

engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()


def validate_username(ctx, param, value):
    if not 1 <= len(value) <= 20:
        raise click.BadParameter(
            "Username must be a string between 1 and 20 characters."
        )
    return value


def validate_email(ctx, param, value):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise click.BadParameter("Invalid email address.")
    return value


@click.command()
@click.option(
    "--username",
    prompt="[Choose a username between 1-20 characters?]",
    type=str,
    callback=validate_username,
    help="Specify your new username between 1 -20 characters.",
)
@click.option(
    "--email",
    prompt="What is your email address?",
    type=str,
    callback=validate_email,
    help="Specify your email address.",
)
def new_user(username, email):
    print(username)
    print(email)


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
