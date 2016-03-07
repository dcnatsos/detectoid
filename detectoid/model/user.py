
from sqlalchemy import Column  # NOQA
from sqlalchemy.types import Integer, Unicode, DateTime  # NOQA

from detectoid.model import DeclarativeBase

class User(DeclarativeBase):
    """
    Twitch user.
    """

    __tablename__ = 'user'

    id_user = Column(Integer, autoincrement=True, primary_key=True)
    """ user db id """
    name = Column(Unicode, nullable=False)
    """ username """
    created = Column(DateTime, nullable=False, index=True)
    """ account creation date """
    updated = Column(DateTime, nullable=False, index=True)
    """ account update date """
    follows = Column(Integer)
    """ count of followed channels """

    def __eq__(self, other):
        return self.name == other.name
