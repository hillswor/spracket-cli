from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
import re
import tabulate
import ipdb


# from existing_user import existing_user
from db.models import Base, User, Bike, StolenBike

database_path = "db/spracket.db"
engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()

current_user = None
current_bike = None

state_abbreviations = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]


######## display_users_bikes ########
def display_users_bikes():
    bikes = current_user.bikes
    if bikes:
        table_data = [
            (
                bike.id,
                bike.brand,
                bike.model,
                bike.year,
                bike.serial_number,
                bike.stolen,
            )
            for bike in bikes
        ]
        headers = ["ID", "Brand", "Model", "Year", "Serial Number", "Stolen"]
        table = tabulate.tabulate(table_data, headers=headers, tablefmt="fancy_grid")
        click.echo(f"\n{current_user.username}'s Bikes:")
        click.echo(
            click.style("\n" + (table) + "\n", fg="green", bg="black", bold=True)
        )
    else:
        click.echo("You have no bikes in your profile.")


###########################################


######## remove_bike method ########


@click.command()
@click.option(
    "--id",
    prompt="Looking at the bike ID's, which bike would you like to remove?",
    type=int,
    help="Specify the ID of the bike you would like to remove.",
)
def remove_bike(id):
    if id in [bike.id for bike in current_user.bikes]:
        bike = session.query(Bike).filter_by(id=id).first()
        session.delete(bike)
        session.commit()
        click.clear()
        click.echo("Bike successfully removed.")
        display_users_bikes()
        main_menu()
    else:
        click.clear()
        click.echo("Bike not found.")
        main_menu()


#############################

######## update_bike method ########


def validate_bike_id(ctx, param, value):
    if value in [bike.id for bike in current_user.bikes]:
        return value
    else:
        raise click.BadParameter("Bike not found.")


def validate_value(ctx, param, value):
    if not isinstance(value, (str, int)):
        raise click.BadParameter("Value must be a string or an integer.")
    return value


def validate_year(ctx, param, value):
    try:
        value = int(value)
    except ValueError:
        raise click.BadParameter("Year must be a 4 digit number.")

    if not isinstance(value, int):
        raise click.BadParameter("Year must be an integer.")
    elif value < 1000 or value > 9999:
        raise click.BadParameter("Year must have exactly four digits.")
    return value


@click.command()
@click.option(
    "--id",
    prompt="Using the bike ID's, which bike would you like to update?",
    type=int,
    callback=validate_bike_id,
    help="Specify the ID of the bike you would like to update.",
)
@click.option(
    "--option",
    prompt="What would you like to update?",
    type=click.Choice(["brand", "model", "year", "serial_number", "stolen"]),
)
@click.option(
    "--value",
    prompt="What would you like to update it to?",
    callback=validate_value,
    help="Specify what you want to update to.",
)
def update_bike(id, option, value):
    bike = session.query(Bike).filter_by(id=id).first()
    if option == "brand":
        bike.brand = value
        session.commit()
        click.clear()
        click.echo("Bike brand successfully updated.")
        display_users_bikes()
        main_menu()
    elif option == "model":
        bike.model = value
        session.commit()
        click.clear()
        click.echo("Bike model successfully updated.")
        display_users_bikes()
        main_menu()
    elif option == "year":
        while True:
            try:
                value = validate_year(
                    None, None, value
                )  # Validate year using the callback
                break  # Break the loop if validation succeeds
            except click.BadParameter as e:
                click.echo(str(e))  # Print the error message
                value = click.prompt(
                    "What would you like to update it to?"
                )  # Re-prompt for the value
        bike.year = value
        session.commit()
        click.clear()
        click.echo("Bike year successfully updated.")
        display_users_bikes()
        main_menu()
    elif option == "serial_number":
        bike.serial_number = value
        session.commit()
        click.clear()
        click.echo("Bike serial number successfully updated.")
        display_users_bikes()
        main_menu()
    elif option == "stolen":
        bike.stolen = value
        session.commit()
        click.clear()
        click.echo("Bike stolen status successfully updated.")
        display_users_bikes()
        main_menu()


####################################

######## report_stolen ########


def validate_state(ctx, param, value):
    if not re.match(r"^[A-Za-z]{2}$", value):
        raise click.BadParameter("Invalid state.")
    elif value.upper() not in state_abbreviations:
        raise click.BadParameter("Invalid state.")

    return value


def validate_zip_code(ctx, param, value):
    if len(value) != 5:
        raise click.BadParameter("Invalid zip code.")

    return value


@click.command()
@click.option(
    "--id",
    prompt="Using the bike ID's, which bike would you like to report stolen?",
    type=int,
    callback=validate_bike_id,
    help="Specify the ID of the bike you would like to report stolen.",
)
@click.option(
    "--date_stolen",
    prompt="What date was the bike stolen(MM-DD-YYYY)?",
    type=click.DateTime(formats=["%m-%d-%Y"]),
    help="Specify the date the bike was stolen.",
)
@click.option(
    "--city",
    prompt="What city was the bike stolen in?",
    type=str,
    help="Specify the city the bike was stolen in.",
)
@click.option(
    "--state",
    prompt="What state was the bike stolen in?",
    type=str,
    callback=validate_state,
    help="Specify the state the bike was stolen in.",
)
@click.option(
    "--zip_code",
    prompt="What ZIP code was the bike stolen in?",
    type=str,
    callback=validate_zip_code,
    help="Specify the ZIP code the bike was stolen in.",
)
def report_stolen(id, date_stolen, city, state, zip_code):
    bike = session.query(Bike).filter_by(id=id).first()
    global current_bike
    current_bike = bike
    bike.stolen = True
    stolen_bike = StolenBike(
        date_stolen=date_stolen,
        city=city,
        state=state,
        zip_code=zip_code,
        user_id=current_user.id,
        bike_id=current_bike.id,
    )
    session.add(stolen_bike)
    session.commit()
    click.clear()
    click.echo("Bike successfully reported stolen.")
    display_users_bikes()
    main_menu()


###############################

######## search_stolen ########


@click.command()
@click.option(
    "--action",
    prompt="Would you like to view all bikes or search by city, state, or ZIP code?",
    type=click.Choice(["all", "city", "state", "zip_code"]),
)
def search_stolen_bikes(action):
    if action == "all":
        stolen_bikes = session.query(StolenBike).all()
        if stolen_bikes:
            table_data = [
                (
                    stolen_bike.bike.id,
                    stolen_bike.date_stolen,
                    stolen_bike.bike.brand,
                    stolen_bike.bike.model,
                    stolen_bike.bike.year,
                    stolen_bike.city,
                    stolen_bike.state,
                    stolen_bike.zip_code,
                )
                for stolen_bike in stolen_bikes
            ]
            headers = [
                "ID",
                "Date Stolen",
                "Brand",
                "Model",
                "Year",
                "City",
                "State",
                "ZIP Code",
            ]
            table = tabulate.tabulate(table_data, headers, tablefmt="fancy_grid")
            click.echo(f"\nStolen Bikes:\n")
            click.echo(
                click.style("\n" + table + "\n", fg="green", bg="black", bold=True)
            )
            main_menu()
        else:
            click.echo("No stolen bikes found.")
            main_menu()
    elif action == "city":
        city = click.prompt("What city would you like to search for?")
        stolen_bikes = session.query(StolenBike).filter_by(city=city).all()
        if stolen_bikes:
            table_data = [
                (
                    stolen_bike.bike.id,
                    stolen_bike.date_stolen,
                    stolen_bike.bike.brand,
                    stolen_bike.bike.model,
                    stolen_bike.bike.year,
                    stolen_bike.bike.serial_number,
                    stolen_bike.city,
                    stolen_bike.state,
                    stolen_bike.zip_code,
                )
                for stolen_bike in stolen_bikes
            ]
            headers = [
                "ID",
                "Date Stolen",
                "Brand",
                "Model",
                "Year",
                "Serial Number",
                "City",
                "State",
                "ZIP Code",
            ]
            table = tabulate.tabulate(table_data, headers, tablefmt="fancy_grid")
            click.echo(f"\nStolen Bikes:\n")
            click.echo(
                click.style("\n" + table + "\n", fg="green", bg="black", bold=True)
            )
            main_menu()
        else:
            click.echo(f"No stolen bikes found in {city}.")
            main_menu()
    elif action == "state":
        state = click.prompt("What state would you like to search for?")
        stolen_bikes = session.query(StolenBike).filter_by(state=state).all()
        if stolen_bikes:
            table_data = [
                (
                    stolen_bike.bike.id,
                    stolen_bike.date_stolen,
                    stolen_bike.bike.brand,
                    stolen_bike.bike.model,
                    stolen_bike.bike.year,
                    stolen_bike.bike.serial_number,
                    stolen_bike.city,
                    stolen_bike.state,
                    stolen_bike.zip_code,
                )
                for stolen_bike in stolen_bikes
            ]
            headers = [
                "ID",
                "Date Stolen",
                "Brand",
                "Model",
                "Year",
                "Serial Number",
                "City",
                "State",
                "ZIP Code",
            ]
            table = tabulate.tabulate(table_data, headers, tablefmt="fancy_grid")
            click.echo(f"\nStolen Bikes:\n")
            click.echo(
                click.style("\n" + table + "\n", fg="green", bg="black", bold=True)
            )
            main_menu()
        else:
            click.echo(f"No stolen bikes found in {state}.")
            main_menu()
    elif action == "zip_code":
        zip_code = click.prompt("What ZIP code would you like to search for?")
        stolen_bikes = session.query(StolenBike).filter_by(zip_code=zip_code).all()
        if stolen_bikes:
            table_data = [
                (
                    stolen_bike.bike.id,
                    stolen_bike.date_stolen,
                    stolen_bike.bike.brand,
                    stolen_bike.bike.model,
                    stolen_bike.bike.year,
                    stolen_bike.bike.serial_number,
                    stolen_bike.city,
                    stolen_bike.state,
                    stolen_bike.zip_code,
                )
                for stolen_bike in stolen_bikes
            ]
            headers = [
                "ID",
                "Date Stolen",
                "Brand",
                "Model",
                "Year",
                "Serial Number",
                "City",
                "State",
                "ZIP Code",
            ]
            table = tabulate.tabulate(table_data, headers, tablefmt="fancy_grid")
            click.echo(f"\nStolen Bikes:\n")
            click.echo(
                click.style("\n" + table + "\n", fg="green", bg="black", bold=True)
            )
            main_menu()
        else:
            click.echo(f"No stolen bikes found in {zip_code}.")
            main_menu()


###############################

######## view_profile ########


def view_profile():
    display_users_bikes()
    main_menu()


##############################

######## main_menu ########


@click.command()
@click.option(
    "--action",
    prompt="Would you like to view your profile, register a new bike, remove a bike from your profile, update one of your bikes, report one of your bikes stolen or search our stolen database",
    type=click.Choice(["view", "register", "remove", "update", "report", "search"]),
)
def main_menu(action):
    click.clear()
    if action == "view":
        view_profile()
    elif action == "register":
        register_new_bike()
    elif action == "remove":
        if current_user.bikes:
            display_users_bikes()
            remove_bike()
        else:
            click.echo("You have no bikes in your profile.")
            main_menu()
    elif action == "update":
        display_users_bikes()
        update_bike()
    elif action == "report":
        if current_user.bikes:
            display_users_bikes()
            report_stolen()
        else:
            click.echo(
                "You have no bikes in your profile.  Please register a bike to report it stolen."
            )
            main_menu()
    elif action == "search":
        search_stolen_bikes()


###########################

######## register new bike methods ########


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
def register_new_bike(brand, model, year, serial_number):
    new_bike = Bike(
        brand=brand.lower(),
        model=model.lower(),
        year=year,
        serial_number=serial_number.lower(),
        user_id=current_user.id,
    )
    session.add(new_bike)
    session.commit()
    click.clear()
    click.echo("Bike successfully added.")
    display_users_bikes()
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
    current_user = session.query(User).filter_by(username=username).first()
    click.echo("User successfully added.")
    click.clear()
    main_menu()


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
def existing_user(username):
    global current_user
    current_user = session.query(User).filter_by(username=username).first()
    click.clear()
    main_menu()


#######################################


######## welcome method ########


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


#################################


if __name__ == "__main__":
    click.clear()
    welcome()
