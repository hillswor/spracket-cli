from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import ipdb

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)

    __table_args__ = (
        UniqueConstraint("username", name="uq_username"),
        UniqueConstraint("email", name="uq_email"),
    )

    bikes = relationship("Bike", backref="user")
    stolen_bikes = relationship("StolenBike", backref="user")

    def __repr__(self):
        return "<User(username='%s', email='%s')>" % (self.username, self.email)


class Bike(Base):
    __tablename__ = "bikes"

    id = Column(Integer, primary_key=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    serial_number = Column(String)
    stolen = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return (
            "<Bike(brand='%s', model='%s', year='%s', serial_number='%s', stolen='%s')>"
            % (
                self.brand,
                self.model,
                self.year,
                self.serial_number,
                self.stolen,
            )
        )


class StolenBike(Base):
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
    __tablename__ = "stolen_bikes"

    id = Column(Integer, primary_key=True)
    date_stolen = Column(String)
    description = Column(String)
    city = Column(String)
    _state = Column(String(2))
    _zip_code = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    bike_id = Column(Integer, ForeignKey("bikes.id"))

    def __init__(self, description, city, state, zip_code):
        self.description = description
        self.city = city
        self.state = state  # Invoke setter method for state
        self.zip_code = zip_code  # Invoke setter method for zip code

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if len(value) != 2:
            raise ValueError("State must be two letters")
        elif value.upper() not in self.state_abbreviations:
            raise ValueError("State must be a valid US state")
        self._state = value

    @property
    def zip_code(self):
        return self._zip_code

    @zip_code.setter
    def zip_code(self, value):
        if not (str(value).isdigit() and len(str(value)) == 5):
            raise ValueError("Zip code must be five numbers")
        self._zip_code = int(value)

    @property
    def date_stolen(self):
        return self._date_stolen

    @date_stolen.setter
    def date_stolen(self, value):
        try:
            parsed_date = click.DateTime(formats=["%m-%d-%Y"]).convert(
                value, None, None
            )
        except click.exceptions.BadParameter:
            raise ValueError("Date stolen must be in the format MM-DD-YYYY")
        self._date_stolen = parsed_date

    def __repr__(self):
        return (
            "<StolenBike(description='%s', city='%s', state='%s', zip_code='%s')>"
            % (
                self.description,
                self.city,
                self.state,
                self.zip_code,
            )
        )

    bike = relationship("Bike", backref=backref("stolen_bikes", uselist=False))
