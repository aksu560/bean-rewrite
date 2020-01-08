from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy_utils as db_utils
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

    def __repr__(self):
        return [self.server_id, self.server_premium, self.server_announce]


Session.configure(bind=engine)