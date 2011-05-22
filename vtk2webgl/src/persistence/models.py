"""
Author: Jan Palach
Contact: palach@gmail.com
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from persistence.database import Base, db_session, engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(20))

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    @staticmethod
    def get_user(email=None, password=None):
        return User.query.filter(User.email==email).first()

    def __repr__(self):
        return '%s' % (self.name)


#class Contacts(Base):
#    """
#    This class represent a friends of a user, they are users too.
#    So this table set two references for users.
#    """
#    __tablename__ = "contacts"
#    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
#    contact_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

#    def __init__(self, user_id=None, contact_id=None):
#        """
#        A constructor with arguments.
#        """
#        self.user_id = user_id
#        self.contact_id = contact_id

#   def __repr__(self):
#        """
#        A string representation for this object.
#       """
#        return 'user_id: %d, contact_id: %d' % (self.user_id, self.contact_id)

class VTKModels(Base):
    __tablename__ = "vtk_models"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(100))
    description = Column(String)
    type = Column(String(50))
    path = Column(String(300))

    def __init__(self,
                 user_id=None,
                 title=None,
                 description=None,
                 model_type=None,
                 path=None):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.type = model_type
        self.path = path

    def __repr__(self):
        return 'Title: %s - Type: %s' % (self.title, self.type)

Base.metadata.create_all(bind=engine)

