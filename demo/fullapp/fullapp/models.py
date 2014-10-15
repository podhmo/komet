import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    Time,
    Unicode,
    Index,
    Text,
    String,
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


# many to many
members_to_teams = sa.Table(
    "members_to_teams", Base.metadata,
    sa.Column("member_id", sa.Integer, sa.ForeignKey("members.id")),
    sa.Column("team_id", sa.Integer, sa.ForeignKey("teams.id")),
)


class Member(Base):
    __tablename__ = "members"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime())
    teams = orm.relationship("Team", backref="members", secondary=members_to_teams)


class Team(Base):
    __tablename__ = "teams"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime())


class Account(Base):
    __tablename__ = 'accounts'

    email = Column(Unicode(64), primary_key=True)
    enabled = Column(Boolean, default=True)
    created = Column(DateTime, nullable=True, default=datetime.now)
    timeout = Column(Time, nullable=False)
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person')


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(32), nullable=False)
    surname = Column(Unicode(32), nullable=False)
    gender = Column(Enum('M', 'F'), nullable=False)
    birthday = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    addresses = relationship('Address')


class PersonGroup(Base):
    __tablename__ = 'pgroups'

    identifier = Column(Unicode, primary_key=True)
    leader = relationship('Person',
                          uselist=False,
                          innerjoin=True,
                          secondary='group_associations')
    executive = relationship('Person',
                             uselist=True,
                             innerjoin=True,
                             secondary='group_associations')
    members = relationship('Person',
                           uselist=True,
                           secondary='group_associations')


class PersonGroupAssociations(Base):

    __tablename__ = 'group_associations'

    group_id = Column(Unicode, ForeignKey(PersonGroup.identifier), primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id), primary_key=True)


class Address(Base):

    __tablename__ = 'addresses'
    __colanderalchemy_config__ = \
        {'title': 'address',
         'description': 'A location associated with a person.',
         'widget': 'dummy'}

    id = Column(Integer, primary_key=True)
    street = Column(Unicode(64), nullable=False)
    city = Column(Unicode(32), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Numeric, nullable=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship(Person)


from sqlalchemy.sql import exists
from komet import ValidationError, custom_data_validation


@custom_data_validation("create", MyModel)
@custom_data_validation("edit", MyModel)
def unique_name(context, params, ob):
    if context.session.query(exists().where(MyModel.name == params["name"])).scalar():
        raise ValidationError({"name": "name is not unique"})
