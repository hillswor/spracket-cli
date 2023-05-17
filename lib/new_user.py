import click
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import User

database_path = "db/spracket.db"

engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()


def validate_username(ctx, param, value):
    if not 1 <= len(value) <= 20:
        raise click.BadParameter(
            "Username must be a string between 1 and 20 characters."
        )

    # Check if the username already exists in the database
    existing_user = session.query(User).filter_by(username=value).first()
    if existing_user:
        raise click.BadParameter(
            "Username already exists. Please choose a different username."
        )

    return value


def validate_email(ctx, param, value):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise click.BadParameter("Invalid email address.")

    # Check if the email address already exists in the database
    existing_user = session.query(User).filter_by(email=value).first()
    if existing_user:
        raise click.BadParameter(
            "Email address already exists. Please enter a different email address."
        )

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
    new_user = User(username=username, email=email)
    session.add(new_user)
    session.commit()
