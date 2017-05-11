# Meme selfbot

# Imports
import discord
import os
import json
import traceback
import glob
import collections
import string
import unidecode

NUMBERS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def emojify(text):
    """Converts text to regional indicators for use in discord"""

    emojified = ""

    for char in text:

        normalized_char = unidecode.unidecode(char.lower())

        if normalized_char in string.ascii_lowercase:
            emojified += ":regional_indicator_{0}: ".format(normalized_char)

        elif char.isnumeric():
            emojified += ":{0}: ".format(NUMBERS[int(char)])

        elif char == " ":
            emojified += "   "

        else:
            emojified += char.replace("!", ":exclamation: ").replace("?", ":question: ")

    return emojified


# Calculate filename similarity score
def filename_matches(keywords, filename):
    """Checks if keywords match filename and returns how many times it matched"""

    # Tokens
    tokens_filename = "".join(filename.split(".")[:-1]).split(" ")

    # How many same tokens
    same = 0.0

    # Loop
    for token_query in keywords:

        for token_filename in tokens_filename:

            if token_query.lower() == token_filename.lower():

                same += 1.0

    # Return similarity score
    return same


class SelfBot(discord.Client):

    def __init__(self):
        """Constructor for SelfBot"""

        # Initialise the discord.Client base class
        super().__init__()

        # Fields of class
        self.config = {}
        self.token = ""
        self.memes = []
        self.meme_paths = []
        self.file_types = []
        self.cwd = os.path.dirname(os.path.realpath(__file__))

    def run_bot(self):

        self.load_config()
        print("Loading bot... This may take a while!")
        self.run(self.token, bot=False)

    async def on_ready(self):
        """Method called when bot has started"""

        # Print start
        print("Starting ...")

        # TODO load game to play from config

        # Print
        print("Started")

    async def on_message(self, message):
        """Method called when new message is received by bot"""

        # Check if sender is self
        if message.author.id != self.user.id:
            return

        # Check if has command prefix
        if not message.content.startswith("~"):  # TODO load prefix from config
            return

        # Parse command & args.
        command = message.content.replace("~", "", 1).split(" ")[0]
        args = message.content.replace("~", "", 1).split(" ")[1:]

        # Execute matching command
        if command == "meme":
            await self.command_meme(args, message.channel)
            await self.delete_message(message)

        elif command == "help":
            await self.command_help(command=" ".join(args) if args else None)
            await self.delete_message(message)

        elif command == "addmemefolder":
            await self.command_addmemefolder(" ".join(args))
            await self.delete_message(message)

        elif command == "removememefolder":
            await self.command_removememefolder(" ".join(args))
            await self.delete_message(message)

        elif command == "addfiletype":
            await self.command_addfiletype(" ".join(args).replace(".", "", 1))  # Remove first dot from filetype
            await self.delete_message(message)

        elif command == "removefiletype":
            await self.command_removefiletype(" ".join(args).replace(".", "", 1))  # " (ditto)
            await self.delete_message(message)

        elif command == "emojify":
            await self.command_emojify(message)

        elif command == "reload":
            await self.command_reload()
            await self.delete_message(message)

        # TODO do not delete but edit original message with response to command

    # -- Commands -- #
    async def command_meme(self, keywords: list, channel: discord.Channel):
        """Sends closest matching meme to channel"""

        matching = []
        Meme = collections.namedtuple("Meme", ["matches", "filename", "path"])

        # Populate list of matching memes with `Meme` named tuples
        for meme_path in self.memes:

            meme_filename = meme_path.split(os.path.sep)[-1]
            matches = filename_matches(keywords, meme_filename)

            if matches > 0:

                matching.append(Meme(matches, meme_filename, meme_path))

        # Sort matching
        matching.sort(key=lambda x: x.matches)
        matching.reverse()  # Make item with highest matches first instead of last

        # Meme with most matches
        matching_meme = matching[0] if len(matching) > 0 else None

        # Send the meme with the most matches
        if matching_meme:

            print("Sending meme \"{0}\"...".format(matching_meme.filename))

            try:
                await self.send_file(channel, matching[0].path)
                print("... meme \"{0}\" successfully sent!".format(matching_meme.filename))

            # Catch any exceptions from discord, e.g no permission, file too large
            except discord.DiscordException:
                print("Error sending meme \"{0}\": \n{1}".format(matching_meme.filename, traceback.format_exc()))
                print("Was the file too large? Do you have permission to send files?")

                # TODO make gui alert

        else:
            print("No matching memes")  # TODO make gui alert

    async def command_help(self, command: str = None):
        """Shows help"""

        pass  # TODO

    async def command_addmemefolder(self, directory: str):
        """Adds folder to discover memes in"""

        # Check if directory exists and is a directory
        if os.path.isdir(directory):

            # Add meme directory
            self.meme_paths.append(directory)

            # Save & reload config
            self.save_config()
            self.load_config()

            # Print
            print("Meme folder \"{0}\" has successfully been added!".format(directory))  # TODO make gui alert

        else:

            print("Meme folder \"{0}\" does not exist!".format(directory))  # TODO make gui alert

    async def command_removememefolder(self, directory: str):
        """Removes folder to discover memes in"""

        # Check if directory is in meme folders
        if directory in self.meme_paths:

            # Remove from meme paths
            self.meme_paths.remove(directory)

            # Save & reload config
            self.save_config()
            self.load_conifg()

        else:
            pass  # TODO add to exlcuded folders

    async def command_addfiletype(self, filetype: str):
        """Adds file type to list of file types to compare keywords to in command_meme
        `filetype` *without* dot
        """

        # Add to list of filetypes if it is not in filetypes
        if filetype not in self.file_types:
            self.file_types.append(filetype)
            print("Successfully added \".{0}\" to file types!".format(filetype))  # TODO make gui alert

        else:
            print("\".{0}\" was already in file types - no action taken. You can probably ignore this".format(filetype))
            # TODO make gui alert

    async def command_removefiletype(self, filetype: str):
        """Removes file type from list of file types to compare keywords to in command_meme
        `filetype` *without* dot
        """

        # Remove from list of filetypes if it is in filetypes
        if filetype in self.file_types:
            self.file_types.remove(filetype)
            print("Successfully removed \".{0}\" to file types!".format(filetype))  # TODO make gui alert

        else:
            print("\".{0}\" was not in file types - no action taken. You can probably ignore this".format(filetype))
            # TODO make gui alert

    async def command_emojify(self, message: discord.Message):
        """Emojify's given text into regional indicators!
        Edits original message
        """

        print("Emojifying ...") # TODO make gui alert
        await self.edit_message(message, emojify(message.content.replace("~emojify ", "", 1)))

    async def command_reload(self):
        """Reloads config and rediscovers memes in folders"""

        self.load_config()
        print("Reloaded")  # TODO make gui alert

    def discover_memes(self):
        """Populates self.memes"""

        self.memes = []

        for meme_path in self.meme_paths:

            for extension in self.file_types:

                self.memes.extend(glob.glob(os.path.join(meme_path, "**", "*.{0}".format(extension)), recursive=True))

    def load_config(self):
        """Loads config from config.json and supplies defaults if property nonexistent"""

        # Default paths for memes
        default_meme_paths = [os.path.join(os.path.expanduser("~"), "Pictures", "Memes"),
                              os.path.join(self.cwd, "Memes"),
                              os.path.join(self.cwd, "memes"),
                              os.path.join(os.path.expanduser("~"), "pictures", "memes"),
                              os.path.join(os.path.expanduser("~"), "memes"),
                              os.path.join(os.path.expanduser("~"), "Memes")]

        # Try to load the config file
        try:
            self.config = json.load(open(os.path.join(self.cwd, "config.json")))
        except FileNotFoundError:
            self.config = {}

        # Try get token, meme paths, file types, and memes
        self.token = self.config.get("token", self.token)
        meme_paths_raw = self.config.get("meme_directories", self.meme_paths)
        self.file_types = self.config.get("file_types", self.file_types)

        # Assign default values to fields if not loaded from json
        if not self.token:
            self.token = input("Token > ")

        if not self.file_types:
            self.file_types = ["jpg", "jpeg", "png", "gif", "tiff", "bmp"]

        if not meme_paths_raw:
            meme_paths_raw = default_meme_paths

        # Remove dead links from default meme paths i.e nonexistent paths
        self.meme_paths = [meme_path for meme_path in meme_paths_raw if os.path.isdir(meme_path)]

        # "Discover" memes - look in paths for files with matching file types and add them to self.memes
        self.discover_memes()

        # Save config file
        self.save_config()

    def save_config(self):
        """Saves config to config.json"""

        self.config["token"] = self.token
        self.config["meme_directories"] = self.meme_paths
        self.config["file_types"] = self.file_types

        json.dump(self.config, open(os.path.join(self.cwd, "config.json"), "w"))  # Dumps config to json file

sb = SelfBot()
sb.run_bot()