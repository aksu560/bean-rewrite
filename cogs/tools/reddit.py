import configparser
import os
import praw

# Open the .ini file
redditAuth = configparser.ConfigParser()
auth = open(os.getcwd() + "/auth.ini")
redditAuth.read_file(auth)

# Get the credentials from the .ini file
redditId = redditAuth.get("reddit", "id")
redditSecret = redditAuth.get("reddit", "secret")
redditUser = redditAuth.get("reddit", "user")

# Creating the required Reddit object
reddit = praw.Reddit(client_id=redditId, client_secret=redditSecret, user_agent=redditUser)