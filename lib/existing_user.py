import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import User
from new_user import new_user
from register import register
import ipdb

database_path = "db/spracket.db"
engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()


def validate_existing_user(ctx, param, value):
    existing_user = session.query(User).filter_by(username=value).first()
    if existing_user is None:
        choice = click.prompt(
            "Username does not exist. Please enter a valid username or type 'new' to set up an account"
        )
        if choice.lower() == "new":
            new_user()
        else:
            raise click.BadParameter("Invalid choice. Please enter a valid username.")
    return value


@click.command()
@click.option(
    "--username",
    prompt="What is your username?",
    type=str,
    callback=validate_existing_user,
    help="Specify your username.",
)
@click.option(
    "--action",
    prompt="Would you like to register a new bike, remove a previously registered bike, or search the database?",
    type=click.Choice(["register", "remove", "search"]),
    help="Specify if you would like to register a new bike, remove a previously registered bike, or search the database.",
)
def existing_user(username, action):
    if action == "register":
        register()
    elif action == "remove":
        print("REMOVE")
    else:
        print("SEARCH")
