import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

required_items = ["year", "artist", "genre", "album"]
class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(sa.func.lower(Album.artist) == artist.lower()).all() # sa.func.lower позволит делать запрос прописными буквами
    return albums

def album_exists(album):
    """
    Ответит, существует ли запрашиваемый альбом в базе альбомов.
    Проверяет на совпадение по имени артиста, имени альбома и году альбома.
    """
    session = connect_db()
    query = session.query(Album).filter(
        sa.func.lower(Album.artist) == album["artist"].lower(),
        sa.func.lower(Album.album) == album["album"].lower(), 
        Album.year == album["year"])
    return bool(query.count())

def add(album):
    """
    Добавляет данные из словаря album в базу данных
    """
    session = connect_db()
    session.add(Album(**album))
    session.commit()



if __name__ == "__main__":
    session = connect_db()
    print(session.query(Album).count())