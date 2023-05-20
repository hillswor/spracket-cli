from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User


if __name__ == "__main__":
    fake = Faker()
    engine = create_engine("sqlite:///spracket.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    for _ in range(50):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
        )
        session.add(user)

    session.commit()
