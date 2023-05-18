from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
import re
import tabulate


# from existing_user import existing_user
from db.models import Base, User, Bike

database_path = "db/spracket.db"
engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()

current_user = None

######## view_profile ########


def view_profile():
    ipdb.set_trace()


##############################

######## main_menu ########


@click.command()
@click.option(
    "--action",
    prompt=f"Would you like to add a new bike, search for a bike to purchase, view your profile, or exit?",
    type=click.Choice(["add", "search", "view", "exit"]),
    help="Specify if you would like to add a new bike, search for a bike to purchase, view your profile, or exit.",
)
def main_menu(action):
    if action == "add":
        add_new_bike()
    elif action == "search":
        print("search")
    elif action == "view":
        view_profile()
    elif action == "exit":
        print("exit")


###########################

######## add new bike methods ########


@click.command()
@click.option(
    "--brand",
    prompt="What is the brand of the bike?",
    type=str,
    help="Specify the brand of the bike.",
)
@click.option(
    "--model",
    prompt="What is the model of the bike?",
)
@click.option(
    "--year",
    prompt="What is the year of the bike?",
    type=int,
    help="Specify the year of the bike.",
)
@click.option(
    "--serial_number",
    prompt="What is the serial number of the bike?",
    type=str,
    help="Specify the serial number of the bike.",
)
def add_new_bike(brand, model, year, serial_number):
    user_id = session.query(User).filter_by(username=current_user).first().id
    new_bike = Bike(
        brand=brand.lower(),
        model=model.lower(),
        year=year,
        serial_number=serial_number.lower(),
        user_id=user_id,
    )
    session.add(new_bike)
    session.commit()
    click.echo("Bike successfully added.")
    main_menu()


######################################

######## new_user methods ########


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
    prompt="Choose a username between 1-20 characters?",
    type=str,
    callback=validate_username,
    help="Specify your new username between 1-20 characters.",
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
    global current_user
    current_user = username
    new_user_menu()


@click.command()
@click.option(
    "--action",
    prompt=f"Thank you for registering. Would you like to add a new bike or search for a bike to purchase?",
    type=click.Choice(["add", "search"]),
    help="Specify if you would like to add a new bike or search for a bike to purchase.",
)
def new_user_menu(action):
    if action == "add":
        add_new_bike()
    elif action == "search":
        print("search")


#################################

######## existing user methods ########


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
    prompt="Would you like to add a new bike, remove a previously registered bike, search for a bike to purchase, or view your profile?",
    type=click.Choice(["add", "remove", "search", "view"]),
    help="Specify if you would like to add a new bike, remove a previously registered bike, search the database, or view your profile.",
)
def existing_user(username, action):
    global current_user
    current_user = username
    if action == "add":
        add_new_bike()
    elif action == "remove":
        print("remove")
    elif action == "search":
        print("search")
    elif action == "view":
        view_profile()


#######################################


######## welcome methods ########


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
        click.clear()
        new_user()
    else:
        existing_user()


#################################


if __name__ == "__main__":
    click.clear()
    welcome()
