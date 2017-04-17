# Meme Bot
This selfbot allows you to send memes and files from your computer via discord, with a simple command.

# Documentation
All documentation can be found [here](https://github.com/Restioson/meme-bot/wiki)

## Howto
![Howto gif](https://raw.githubusercontent.com/Restioson/meme-bot/master/meme-bot.gif "Demonstration showing how to send memes using the meme bot")

*Note: the gif is slow due to my internet speed. If your internet is faster, it will send the memes faster.*

# Installation

## Windows
- Install [Python](https://www.python.org/) 3.5 or higher and add it to your `PATH`. On Windows, during the installation you can tick an option to do this. Here is a [nice guide](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/) on how to do this! Make sure that you *remove* earlier versions of Python *from your* `PATH`.

- In a shell or `cmd` window, type in `python --version`. If the output looks something like `Python3...` then you are ok! If the output says that you are running Python 2, make sure you have removed this from your `PATH`.

- Install pip (if not preinstalled) and add it to your `PATH` (or equivalent). 

- In a shell or `cmd` window, type in `pip3 install discord.py` and press enter. This step is **very important**!. If it gives you an error like `Error: no such command "pip3"` make sure that you have added Python to your path correctly.

- Download the latest stable release of Meme-Bot from [here](https://github.com/Restioson/meme-bot/releases/latest)

- Extract it

- Open a shell or `cmd` window

- `cd` to where the downloaded folder is - under Windows, this means that you type in `cd C:\Users\YOUR_USERNAME_HERE\Downloads`. Don't forget to replace `YOUR_USERNAME_HERE` with your Windows username

- Type `cd meme-bot-master` and press enter. Do this *twice*.

- At this stage I reccommend that you create the folder `path/to/home/directory/Pictures/Memes`, or, under Windows, `C:\Users\YOUR_USERNAME_HERE\Pictures\Memes` and put all your memes in here. Don't forget to replace `YOUR_USERNAME_HERE` with your Windows username

- To run the bot, type in `python meme-bot.py`. 

- At the `Token > ` prompt, paste in your Discord user API Token

- To add a new folder of memes to this bot, you must open the `config.json` file it has created the first time it is run

- Find the section which says something like `"meme_directories": ["C:\\..."`. Just *before* the closing `]`, type `,"C:\\Path\\To\\Memes"`. Replace `C:\\Path\\To\\Memes` with whichever folder you want to add. **NOTE: replace all your normal backslashes with *double* backslashes or *this will not work*. You will get a *Unicode error***

## Linux
I am going to assume that you are fairly profficient in computers. I will write a better guide when I get the chance, but for now, here it is:

- Install python3.5 if not already installed

- Verify that python3.5 is working

- Verify pip3 is working - this should come with python

- Type `pip3 install discord.py`

- Clone github.com/Restioson/meme-bot

- CD to the cloned directory

- To run the bot, type `python meme-bot.py`

- To add a new meme directory, add it to the `config.json` which is generated on first run, under `meme_directories`


The bot will only work if it is running. You can set it up to start on startup if you prefer, but this is outside the domain of this tutorial.

# Compatability
This selfbot *should* be compatible on all OSes supporting Python 3.5 or later. However, Meme Bot will only auto-discover memes in `C:\Users\user\Pictures\Memes` on Windows.

# Reporting an issue
To report a bug/issue, please add it to the [issue tracker](https://github.com/Restioson/meme-bot/issues). Please check to see if it hasn't already been reported *before* posting.

# Contributing
If you would like to contribute to this project, fork it, commit your changes, and submit a pull request.

# FAQ
**Help! What is a Discord user API token?**

This is your secret string that you can use to let selfbots send messages and do other things on behalf of you. You will need to give this to the bot so it can a) read messages send to you to listen for commands and b) send memes for you. I won't send this to anyone else, nor read any of your messages, but you can check it out in the [code](https://github.com/Restioson/meme-bot/blob/master/meme-bot.py#L41) if you like.

**How do I get it?**

There is a guide [here](https://www.reddit.com/r/discordapp/comments/5ncwpv/localstorage_missing/dcalpi1/). Thank you to [/u/DJScias](https://www.reddit.com/user/DJScias) for this wonderul short tutorial.

**How do I add a meme folder?**

In future I will add a command to do this. You need to open your `config.json`, which will be in the same folder as Meme-Bot. It will look something like this:
```json
{"token":"someuntintelligblething","meme_directories"=["path/to/memes","path/to/memes2",...],"file_types"=["jpg","png"...]}
```
Find the bit which says `"meme_directories=["path/to/memes",...]`. Just before the `]` bracket, put a comma, then a quotation mark. Now, type the directory you want to add. Type another quotation mark and save the file.

**How do I report a bug?**

The [issue tracker](https://github.com/Restioson/meme-bot/issues).

**I have a suggestion!**

[Create an issue](https://github.com/Restioson/meme-bot/issues) with the [enhancement](https://github.com/Restioson/meme-bot/labels/enhancement) label.

**How does [thing x] work?**

Have you read this page? Have you checked the wiki? If the answer is yes to both, feel free to [create an issue](https://github.com/Restioson/meme-bot/issues/new) with the [question](https://github.com/Restioson/meme-bot/labels/question) tag.

# Special Thanks
Special thanks to MegaMeltdown for helping with the docs and testing the bot!

# Contact & Help

Feel free to contact me on discord: Restioson#8323
