from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, LargeBinary, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import pickle
import subprocess
from datetime import datetime
import configparser
import os

cfgParser = configparser.ConfigParser()
auth = open(os.getcwd() + "/auth.ini")
cfgParser.read_file(auth)
dbpswd = cfgParser.get("db", "pswd")

# Replace the ID with your own
bot_owner_id = "114796980739244032"
print(f"Bot owner is: {bot_owner_id}")
print(dbpswd)

db_url = f"postgresql://postgres:{dbpswd}@localhost/beanbase"

Session = sessionmaker()

# Create the database if it does not exist
if not database_exists(db_url):
    create_database(db_url)

engine = create_engine(db_url)

# Declaring the base class for declarative structures
Base = declarative_base()


# Servers table
class Servers(Base):
    __tablename__ = 'servers'

    server_id = Column('server_id', String(20), primary_key=True)
    server_level = Column('server_level', Integer)
    date_added = Column('date_added', DateTime)
    settings = Column('settings', LargeBinary)

    admins = relationship("ServerAdmins", back_populates='servers', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return [self.server_id, self.server_level, self.date_added, pickle.loads(self.settings),
                pickle.loads(self.settings)]


# Server Admins table
class ServerAdmins(Base):
    __tablename__ = 'server_admins'

    server_id = Column('server_id', String(20), ForeignKey('servers.server_id'))
    user_id = Column('role_id', String(20), primary_key=True)
    servers = relationship("Servers", back_populates='admins')

    def __repr__(self):
        return [self.server_id, self.user_id]


# Custom commands table
class CustomCommand(Base):
    __tablename__ = 'custom_commands'

    server_id = Column('server_id', String(20), ForeignKey('servers.server_id'))
    command_id = Column('command_id', Integer, primary_key=True, autoincrement=True)
    command_name = Column('command_name', String(64))
    output_text = Column('output_text', String(1000))
    help_text = Column('help_text', String(32))

    def __repr__(self):
        return [self.server_id, self.command_name, self.output_text, self.help_text]


# Quotes table
class Quote(Base):
    __tablename__ = 'quote'

    server_id = Column('server_id', String(20), ForeignKey('servers.server_id'))
    quote_id = Column('quote_id', Integer, primary_key=True, autoincrement=True)
    text = Column('text', String(1500))
    user = Column('user', String(35))

    def __repr__(self):
        return [self.server_id, self.command_name, pickle.loads(self.output_object), self.help_text]


# Bot Admins table
class BotAdmins(Base):
    __tablename__ = 'bot_admins'

    user_id = Column('server_id', String(20), primary_key=True)
    admin_since = Column('admin_since', DateTime)
    made_admin_by = Column('made_admin_by', String(20))

    def __repr__(self):
        return [self.user_id, self.admin_since, self.made_admin_by]


Base.metadata.create_all(engine)
Session.configure(bind=engine)

db = Session()
db.commit()


# Function for adding new servers to the table. Returns True once ran
def AddServer(server_id):
    db.add(Servers(server_id=server_id,
                   server_level=1,
                   date_added=datetime.now(),
                   settings=pickle.dumps({})))
    db.commit()
    return True


# Function for querying a server entry from the servers table. Returns a list object
# [server_id: str, server_level: int, ], or None if server was not found from the table.
def GetServer(wanted_server_id):
    for queryresult in db.query(Servers).filter(Servers.server_id == wanted_server_id):
        return {"id": queryresult.server_id,
                "level": queryresult.server_level,
                "date": queryresult.date_added,
                "settings": pickle.loads(queryresult.settings)}
    return None


# Update the server's level. Right now only used for uncapping quote and custom command amount
def UpdateServerLevel(wanted_server_id, server_level):
    for queryresult in db.query(Servers).filter(Servers.server_id == wanted_server_id):
        queryresult.server_level = server_level
        db.commit()
    return None


# Function for removing a server entry from the database. Returns True if removal was successful, False if not.
def RemoveServer(wanted_server_id):
    for queryresult in db.query(Servers).filter(Servers.server_id == wanted_server_id):
        db.delete(queryresult)
        db.commit()
        return True
    return False


# Returns the settings object for specified server
def GetServerSettings(server):
    for queryresult in db.query(Servers).filter(Servers.server_id == server):
        return pickle.loads(queryresult.settings)


# Function for retrieving all servers from the servers table. Returns a list object with server IDs
def GetAllServers():
    output = []
    for queryresult in db.query(Servers):
        output.append(queryresult.server_id)
    return output


# Add a new bot level administrator. Returns True if successful, False if not
def AddBotAdmin(granted_user_id, granter_id):
    for result in db.query(BotAdmins):
        if result.user_id == granted_user_id:
            return False

    new_admin = BotAdmins(user_id=granted_user_id, admin_since=datetime.now(), made_admin_by=granter_id)
    db.add(new_admin)
    db.commit()
    print(f"New admin {granted_user_id} added by {granter_id}")
    return True


# More things we run on load. These are here, because they rely on functions defined earlier
bot_admins = []
for result in db.query(BotAdmins):
    bot_admins.append(result.user_id)
print(f"Bot admins are: {str(bot_admins)}")

if bot_owner_id not in bot_admins:
    AddBotAdmin(bot_owner_id, "Bean")


# Remove a bot level administrator. Returns True if successful, False if not
def RemoveBotAdmin(removed_id, remover_id):
    for result in db.query(BotAdmins).filter(BotAdmins.user_id == removed_id):
        db.delete(result)
        db.commit()
        print(f"Admin {removed_id} removed by {remover_id}")
        return True
    return False


# Return all bot level administrators
def GetBotAdmins():
    output = []
    for result in db.query(BotAdmins):
        output.append(result.user_id)
    return output


# Back up the database
def Backup():
    subprocess.run("/vagrant/cogs/tools/backup.sh", shell=True)


# Add a custom command into the database
def AddCustomCommand(server, command, content, help):
    for result in db.query(CustomCommand):
        if result.command_name == command:
            return False

    new_command = CustomCommand(server_id=server, command_name=command, output_text=content, help_text=help)
    db.add(new_command)
    db.commit()
    print(f"New custom command {command}: {content} added for server {server}")
    return True


# Get all custom commands for specified server in format [[Command1 ID, Command1 name, Command1 Output,
# Command1 Help], [Command2 ID]...]
def GetCustomCommands(server):
    output = []
    for queryresult in db.query(CustomCommand).filter_by(server_id=server):
        output.append([queryresult.command_id,
                       queryresult.command_name,
                       queryresult.output_text,
                       queryresult.help_text])
    if not output:
        output = None
    return output


# Delete a custom command. Returns None if no commands were found, True if a command was deleted, or False if
# specified command was not found
def RemoveCustomCommand(server, command):
    for query_result in db.query(CustomCommand).filter(CustomCommand.server_id == server):
        if query_result.command_name == command:
            db.delete(query_result)
            db.commit()
            return True

    return False


# Add a new server level administrator. Returns True if successful, False if not
def AddServerAdmin(server, granted_user_id):
    for result in db.query(BotAdmins).filter(ServerAdmins.server_id == server):
        if result.user_id == granted_user_id:
            return False

    new_admin = ServerAdmins(server_id=server, user_id=granted_user_id)
    db.add(new_admin)
    db.commit()
    return True


# Remove a server level administrator. Returns True if successful, False if not
def RemoveServerAdmin(server, removed_id):
    for result in db.query(ServerAdmins).filter(ServerAdmins.server_id == server):
        if result.user_id == removed_id:
            db.delete(result)
            db.commit()
            return True
    return False


# Return a list of all server level administrators
def GetServerAdmins(server):
    output = []
    for result in db.query(ServerAdmins).filter(ServerAdmins.server_id == server):
        output.append(result.user_id)
    return output


# Add a new quote to the DB
def AddQuote(server, user, quote_text):
    new_quote = Quote(server_id=server, text=quote_text, user=user)
    db.add(new_quote)
    db.commit()
    return True


# Remove a quote from the DB
def RemoveQuote(server, quote):
    for query_result in db.query(Quote).filter(Quote.quote_id == quote):
        if query_result.server_id == server:
            db.delete(query_result)
            db.commit()
            return True
        return False


# Get all quotes from a particular server
def GetQuotes(server):
    output = []
    for result in db.query(Quote).filter(Quote.server_id == server):
        output.append([result.text, result.user, result.quote_id])
    return output
