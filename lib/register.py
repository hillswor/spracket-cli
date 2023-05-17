import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Bike
import ipdb

database_path = "db/spracket.db"
engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()


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
def register(brand, model, year, serial_number):
    new_bike = Bike(
        brand=brand.lower(),
        model=model.lower(),
        year=year,
        serial_number=serial_number.lower(),
    )
    session.add(new_bike)
    session.commit()
    click.echo("Bike successfully registered.")
