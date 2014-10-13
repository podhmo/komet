from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey
)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default="", nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", backref="users", uselist=False)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default="", nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)

from sqlalchemy.sql import exists
from komet import ValidationError, custom_data_validation


@custom_data_validation("create", MyModel)
@custom_data_validation("edit", MyModel)
def unique_name(context, params, ob):
    if context.session.query(exists().where(MyModel.name == params["name"])).scalar():
        raise ValidationError({"name": "name is not unique"})
