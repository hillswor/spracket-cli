from faker import Faker
import ipdb
from datetime import datetime
import random as r
from random import choice as rc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Bike, StolenBike

fake = Faker()
engine = create_engine("sqlite:///spracket.db")
Session = sessionmaker(bind=engine)
session = Session()


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


def delete_records():
    session.query(User).delete()
    session.query(Bike).delete()
    session.query(StolenBike).delete()
    session.commit()


def create_users():
    for _ in range(50):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
        )
        session.add(user)

    session.commit()


def create_bikes():
    bikes = []
    for _ in range(85):
        bike = Bike(
            brand=fake.company(),
            model=fake.word(),
            year=fake.year(),
            serial_number=fake.ean8(),
            stolen=rc(
                [True, False]
            ),  # Initialize all bikes as stolen or not stolen randomly
        )
        bikes.append(bike)

    session.add_all(bikes)
    session.commit()


def relate_bikes_to_users():
    users = session.query(User).all()
    bikes = session.query(Bike).all()
    for bike in bikes:
        bike.user = rc(users)
        session.add(bike)
    session.commit()


def create_stolen_bikes():
    stolen_bikes = session.query(Bike).filter_by(stolen=True).all()

    for stolen_bike in stolen_bikes:
        stolen_bike = StolenBike(
            date_stolen=datetime.strptime(fake.date(), "%Y-%m-%d").strftime("%m-%d-%Y"),
            city=fake.city(),
            state=r.choice(state_abbreviations),
            zip_code=fake.zipcode(),
            user_id=stolen_bike.user_id,
            bike_id=stolen_bike.id,
        )
        session.add(stolen_bike)
    session.commit()


if __name__ == "__main__":
    delete_records()
    create_users()
    create_bikes()
    relate_bikes_to_users()
    create_stolen_bikes()
