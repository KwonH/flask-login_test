from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'user'
    user_id = Column(String(255), primary_key=True)
    nickname = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created     =   Column(DateTime)
    modified    =   Column(DateTime)

    def __init__(self, user_id=None, nickname=None, password=None):
        self.user_id    = user_id
        self.nickname   = nickname
        self.password   = password
 
    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)


    def is_authenticated(self) :
        return True

    def is_active(self) :
        return True

    def is_anonymous(self) :
        return True

    def get_id(self) :
        return self.user_id



