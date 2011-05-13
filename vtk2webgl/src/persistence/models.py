"""
Author: Jan Palach
Contact: palach@gmail.com
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from persistence.database import Base, db_session, engine


class User(Base):
    """
    This class represent a user entity in database,
    it has the following information:
    - user_id: Primary key of the table.
    - name: The complete name of the user.
    - email: An email for authentication and contact.
    - password: A password for authentication.
    """
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(20))

    def __init__(self, name=None, email=None, password=None):
        """
        A constructor with arguments.
        """
        self.name = name
        self.email = email
        self.password = password

    @staticmethod
    def get_user(email=None, password=None):
        return User.query.filter(User.email==email).first()

    def __repr__(self):
        """
        A string representation for this object.
        """
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

class VisualModels(Base):
    """
    This class represent a table for 3D Models. It's has the following fields:
    - visual_model_id: A primary key for table.
    - user_id: The owner of the 3D model.
    - title: The title, short description for 3D model.
    - description: A detailed description for 3D model.
    - model_type: The type of the model, for example, vtkUnstrucuredGrid,
                  vtkPolyData, vtkStructuredGrid, etc. This field is very
                  important to determinate how the model file localized in
                  field path, will be read.
    - path: The localization of 3D model file.
    """
    __tablename__ = "visual_models"
    visual_model_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    title = Column(String(100))
    description = Column(String)
    model_type = Column(String(50))
    path = Column(String(200))

    def __init__(self, user_id=None,
                 title=None, description=None, model_type=None,
                 path=None):
        """
        A constructor with arguments.
        """
        self.user_id = user_id
        self.title = title
        self.description = description
        self.model_type = model_type
        self.path = path

    def __repr__(self):
        """
        A string representation for this object.
        """
        return '%s' % self.title

Base.metadata.create_all(bind=engine)

