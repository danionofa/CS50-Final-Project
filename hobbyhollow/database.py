from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, LargeBinary, PickleType
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///hobbies.db', connect_args={'check_same_thread': False})
db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)
    db_session.commit()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.id, self.username, self.password!r}>'


class Hobby(Base):
    __tablename__ = 'hobbies'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    overview = Column(String, nullable=False)
    img = Column(String)
    hobby_id = Column(Integer, nullable=False)
    genres = Column(String)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __init__(self, name=None, overview=None, img=None, hobby_id=None, genres=None, user_id=None):
        self.name = name
        self.overview = overview
        self.img = img
        self.hobby_id = hobby_id
        self.genres = genres
        self.user_id = user_id

    def __repr__(self):
        return f'<User {self.id, self.name, self.genres!r}>'
