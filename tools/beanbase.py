from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy_utils as db_utils
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle

Session = sessionmaker()

# Create the database if it does not exist
if not db_utils.database_exists('mysql://root:root@localhost/beanbase'):
    db_utils.create_database('mysql://root:root@localhost/beanbase')

engine = create_engine('mysql://root:root@localhost/beanbase')

# Declaring the base class for declarative structures
Base = declarative_base()


# Servers table
class Servers(Base):
    __tablename__ = 'servers'

    server_id = Column(String(17), primary_key=True)
    server_premium = Column('Premium Server', Boolean)
    server_announce = Column('Announcements enabled', Boolean)
    disabled_commands = Column('Disabled Commands', String(10000))

    def __repr__(self):
        return [self.server_id, self.server_premium, self.server_announce, pickle.loads(self.disabled_commands)]


Base.metadata.create_all(engine)
Session.configure(bind=engine)

db = Session()
db.commit()


# Function for adding new servers to the table
def AddServer(server_id):
    db.add(Servers(server_id=server_id,
                   server_premium=False,
                   server_announce=False,
                   disabled_commands=pickle.dumps([])))
    db.commit()


# Function for querying a server from the table
def GetServer(server_id):
    queryresult = db.query(Servers).filter(server_id == server_id)
    return [queryresult.server_id,
            queryresult.server_premium,
            queryresult.server_announce,
            pickle.loads(queryresult.disabled_commands)]


# Function for toggling premium on a server
def TogglePremium(server_id):
    queryresult = db.query(Servers).filter(server_id == server_id)
    targetvalue = not queryresult.server_premium
    queryresult.server_premium = targetvalue
    db.commit()
    return targetvalue


# Function for toggling announcements on a server
def ToggleAnnouncements(server_id):
    queryresult = db.query(Servers).filter(server_id == server_id)
    targetvalue = not queryresult.server_announce
    queryresult.server_premium = targetvalue
    db.commit()
    return targetvalue
