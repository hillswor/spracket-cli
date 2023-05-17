import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import User
import ipdb

database_path = "db/spracket.db"
engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()


@click.command()
@click.option(
    "--username",
    prompt="What is your username?",
    type=str,
    help="Specify your username.",
)
@click.option(
    "--action",
    prompt="Would you like to register a new bike, remove a previously registered bike, or search the database?",
    type=click.Choice(["register", "remove", "search"]),
    help="Specify if you would like to register a new bike, remove a previously registered bike, or search the database.",
)
def existing_user(username, action):
    ipdb.set_trace()
