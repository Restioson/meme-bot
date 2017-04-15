# Meme selfbot

# Imports
import discord
import asyncio
import os
import itertools
import json


# Client
client = discord.Client()

# CWD
cwd = os.path.dirname(os.path.realpath(__file__))

# Variables
config = {}
token = ""
memes = []
meme_paths = []
file_types = []


# On ready
@client.event
async def on_ready():

    # Print start
    print("Starting ...")

    # Change game
    await client.change_presence(game=discord.Game(name="with spicy memes"))

    # Print
    print("Started")


# Send meme command
@client.event
async def on_message(message: discord.Message):

    # Global
    global meme_paths

    # Check sender
    if str(message.author) != str(client.user):
        return

    # Check command
    if message.content.split(" ")[0] == "~meme":

        # Check right number of args
        if not len(message.content.split(" ")) > 1:

            # Delete message if not
            await client.delete_message(message)

            # Return
            return

        # Meme name
        meme = " ".join(message.content.split(" ")[1:])

        # Find matching memes
        matching = [meme_file_path for meme_file_path in memes if meme.replace("_", " ") in meme_file_path]

        # Send first matching meme (if exists)
        if len(matching) > 0:
            print("Sending meme ", matching[0].split(os.path.sep)[-1])
            await client.send_file(message.channel, matching[0])

        else:
            print("No matching memes")

        # Delete command message
        await client.delete_message(message)

    # Check command
    elif message.content.split(" ")[0] == "reload":

        # Reload config
        reload_config()

        for meme_path in meme_paths:
            memes.extend([file_name for file_name in
                          list(itertools.chain(*
                                               [[os.path.join(root, file) for file in files]
                                                for root, subdirectories, files in os.walk(meme_path)]))
                          if file_name.split(".")[0] in file_types])


# Reload config
def load_config():

    # Globals
    global config
    global token
    global memes
    global meme_paths
    global file_types

    # Set all variables to be loaded to default
    config = {}
    token = ""
    meme_paths_raw = []
    memes = []
    file_types = []

    # Try to load the config file
    try:
        config = json.load(open(os.path.join(cwd, "config.json")))

    except FileNotFoundError:
        config = {}

    # Try get token, meme paths, file types, and memes

    try:
        token = config["token"]
        meme_paths_raw = config["meme_directories"]
        file_types = config["file_types"]

    except KeyError:
        token = input("Token > ")
        if os.name == "nt":
            meme_paths_raw = [os.path.join(os.path.expanduser("~"), "Pictures", "Memes"), os.path.join(cwd, "Memes")]
        file_types = ["jpg", "jpeg", "png", "gif", "tiff"]

    # Filter out meme paths that do not exists
    meme_paths = [meme_path for meme_path in meme_paths_raw if os.path.isdir(meme_path)]

    # Populate memes
    for meme_path in meme_paths:
        memes.extend([file_name for file_name in
                      list(itertools.chain(*
                                           [[os.path.join(root, file) for file in files]
                                            for root, subdirectories, files in os.walk(meme_path)]))
                      if file_name.split(".")[0] in file_types])

    # Save config file
    config["token"] = token
    config["meme_directories"] = meme_paths
    config["file_types"] = file_types
    json.dump(config, open(os.path.join(cwd, "config.json"), "w"))


# Reload config
def reload_config():

    # Globals
    global config
    global memes
    global meme_paths
    global file_types

    # Set all variables to be loaded to default
    config = {}
    meme_paths_raw = []
    memes = []
    file_types = []

    # Try to load the config file
    try:
        config = json.load(open(os.path.join(cwd, "config.json")))

    except FileNotFoundError:
        config = {}

    # Try get token, meme paths, file types, and memes

    try:
        meme_paths_raw = config["meme_directories"]
        file_types = config["file_types"]

    except KeyError:
        if os.name == "nt":
            meme_paths_raw = [os.path.join(os.path.expanduser("~"), "Pictures", "Memes"), os.path.join(cwd, "Memes")]
        file_types = ["jpg", "jpeg", "png", "gif", "tiff"]

    # Filter out meme paths that do not exists
    meme_paths = [meme_path for meme_path in meme_paths_raw if os.path.isdir(meme_path)]

    # Populate memes
    for meme_path in meme_paths:
        memes.extend([file_name for file_name in
                      list(itertools.chain(*
                                           [[os.path.join(root, file) for file in files]
                                            for root, subdirectories, files in os.walk(meme_path)]))
                      if file_name.split(".")[0] in file_types])

    # Save config file
    config["token"] = token
    config["meme_directories"] = meme_paths
    config["file_types"] = file_types
    json.dump(config, open(os.path.join(cwd, "config.json"), "w"))

# Load config
load_config()

# Run bot
client.run(token, bot=False)
