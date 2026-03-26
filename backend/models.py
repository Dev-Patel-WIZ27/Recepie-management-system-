from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)

class FamilyGroup(Base):
    __tablename__ = "family_groups"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)

    members = relationship("FamilyMember", back_populates="group")
    posts = relationship("Post", back_populates="group")

class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String, default="member")
    group_id = Column(Integer, ForeignKey("family_groups.id"))

    group = relationship("FamilyGroup", back_populates="members")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    content = Column(Text)
    time_posted = Column(String)
    group_id = Column(Integer, ForeignKey("family_groups.id"))

    group = relationship("FamilyGroup", back_populates="posts")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    ingredients = Column(JSON) # Lists of strings
    image = Column(String)
    time = Column(String)

class LoginRecord(Base):
    __tablename__ = "login_records"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, index=True)
    name = Column(String, nullable=True)
    timestamp = Column(String)
