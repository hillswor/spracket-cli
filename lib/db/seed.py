from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User


if __name__ == "__main__":
    fake = Faker()
    engine = create_engine("sqlite:///spracket.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    for _ in range(100):
        user = User(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        session.add(user)

    session.commit()
