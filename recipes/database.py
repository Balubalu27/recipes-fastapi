from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from recipes.settings import settings


engine = create_engine(settings.database_url)

# Base.metadata.create_all(engine)  -> Для создания таблиц в БД

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False
)


def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()
