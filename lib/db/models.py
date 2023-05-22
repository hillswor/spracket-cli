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
import click
import re
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
    __tablename__ = "stolen_bikes"

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

    id = Column(Integer, primary_key=True)
    date_stolen = Column(String)
    city = Column(String)
    state = Column(String(2))
    zip_code = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    bike_id = Column(Integer, ForeignKey("bikes.id"))

    def __repr__(self):
        return (
            "<StolenBike(date_stolen='%s', city='%s', state='%s', zip_code='%s')>"
            % (
                self.date_stolen,
                self.city,
                self.state,
                self.zip_code,
            )
        )

    bike = relationship("Bike", backref=backref("stolen_bikes", uselist=False))
