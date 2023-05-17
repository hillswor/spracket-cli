from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
from new_user import new_user
from existing_user import existing_user
from db.models import Base, User, Bike

database_path = "db/spracket.db"

engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()


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
        success = new_user()
        if success:
            # New user created successfully, continue with welcome()
            existing_user()
        else:
            # New user creation failed, exit the program or handle the error
            click.echo("Failed to create a new user. Exiting...")
            return
    else:
        existing_user()

    # Continue with the rest of the welcome() logic
    # ...


if __name__ == "__main__":
    welcome()
