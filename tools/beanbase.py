from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, LargeBinary, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import pickle
from datetime import datetime

Session = sessionmaker()

# Create the database if it does not exist
if not database_exists('mysql://root:root@localhost/beanbase'):
    create_database('mysql://root:root@localhost/beanbase')

engine = create_engine('mysql://root:root@localhost/beanbase')

# Declaring the base class for declarative structures
Base = declarative_base()


# Servers table
class Servers(Base):
    __tablename__ = 'servers'

    server_id = Column('server_id', String(20), primary_key=True)
    server_level = Column('premiu', )
    date_added = Column('Date server added the bot', DateTime)
    settings = Column('Settings', LargeBinary)

    roles = relationship("Role", back_populates='servers', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return [self.server_id, self.server_level, self.date_added, pickle.loads(self.settings),
                pickle.loads(self.settings)]


# Roles table
class Role(Base):
    __tablename__ = 'role'

    server_id = Column('Server ID', String(20), ForeignKey('servers.server_id'))
    role_id = Column('Role ID', String(20), primary_key=True)
    perms_object = Column('Permissions Object', LargeBinary)
    servers = relationship("Servers", back_populates='roles')

    def __repr__(self):
        return [self.server_id, self.role_id, pickle.loads(self.perms_object)]


# Custom commands table
class Custom_command(Base):
    __tablename__ = 'custom_command'

    server_id = Column('Server ID', String(20), ForeignKey('servers.server_id'))
    command_id = Column('Command ID', Integer, primary_key=True)
    command_name = Column('Command Name', String(64))
    output_object = Column('Output Object', LargeBinary)
    help_text = Column('Help Text', String(32))

    def __repr__(self):
        return [self.server_id, self.command_name, pickle.loads(self.output_object), self.help_text]


# Quotes table
class Quote(Base):
    __tablename__ = 'quote'

    server_id = Column('Server ID', String(20), ForeignKey('servers.server_id'))
    quote_id = Column('Quote ID', Integer, primary_key=True)
    text = Column('Text', String(1500))
    help_text = Column('Help Text', String(32))

    def __repr__(self):
        return [self.server_id, self.command_name, pickle.loads(self.output_object), self.help_text]


Base.metadata.create_all(engine)
Session.configure(bind=engine)

db = Session()
db.commit()


# Function for adding new servers to the table. Returns True if successful.
def AddServer(server_id):
    db.add(Servers(server_id=server_id,
                   server_level=False,
                   date_added=datetime.now(),
                   settings=pickle.dumps({})))
    db.commit()
    return True


# Function for querying a server entry from the servers table. Returns a list object
# [server_id: str, server_level: bool, ], or None if server was not found from the table.
def GetServer(wanted_server_id):
    for queryresult in db.query(Servers).filter(Servers.server_id == wanted_server_id):
        return [queryresult.server_id,
                queryresult.server_level,
                queryresult.date_added,
                pickle.loads(queryresult.settings)]
    return None


# Function for removing a server entry from the database. Returns True if removal was successful, False if not.
def RemoveServer(wanted_server_id):
    for queryresult in db.query(Servers).filter(Servers.server_id == wanted_server_id):
        db.delete(queryresult)
        db.commit()
        return True
    return False


# Function for retrieving all servers from the servers table. Returns a list object with server IDs
def GetAllServers():
    output = []
    for queryresult in db.query(Servers):
        output.append(queryresult.server_id)
    return output
