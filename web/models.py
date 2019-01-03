from sqlalchemy import Column, Integer, Text
from web.database import Base

class Member(Base):
    """
    CREATE TABLE member (
      no INT(11) unsigned NOT NULL AUTO_INCREMENT,
      name text NOT NULL,
      degree text NOT NULL,
      email text NOT NULL,
      homepage text,
      research text,
      PRIMARY KEY (no)
    );
    """
    __tablename__ = "member"

    no = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    degree = Column(Text, nullable=False)
    email = Column(Text)
    homepage = Column(Text)
    research = Column(Text, nullable=False)
    image = Column(Text)

    def __init__(self, name, degree, email, homepage, research, image):
        self.name = name
        self.degree = degree
        self.email = email
        self.homepage = homepage
        self.research = research
        self.image = image