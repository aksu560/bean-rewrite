from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy_utils as db_utils

# Create the database if it does not exist
if not db_utils.database_exists('mysql://root:root@localhost/beanbase'):
    db_utils.database_create('mysql://root:root@localhost/beanbase')

# Declaring the base class for declarative structures
Base = declarative_base()

# Servers table
class Servers(Base):
    __tablename__ = 'servers'

    server_id = Column(String, primary_key=True)
    server_premium = Column('Premium Server', Boolean)
    server_announce = Column('Announcements enabled', Boolean)
