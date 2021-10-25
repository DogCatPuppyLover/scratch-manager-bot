# Scratch Manager Bot 
A Python bot for Scratch that allows managers of a studio to change the title, description, thumbnail, and toggle commenting in a studio via commands in Scratch comments.

This bot has been explicitly banned by the Scratch Team.

## Features
* Easy to use
* Lightweight
* Open-source

## Installing and running the bot
First, you need to install Python. Check if you have Python already installed by running `python version` on the command line. If you don't have it installed, you can compile it from source or install it via an [installer](https://www.python.org/).

Once you install Python, run these commands in the command line to install the required libraries:

```
pip install requests
pip install html
```

Then download [scratch-manager-bot.py](https://github.com/DogCatPuppyLover/scratch-manager-bot/blob/main/scratch-manager-bot.py) from this repository and run `python scratch-manager-bot` in the command line.

It will then ask you for your Scratch username, password, the ID of the studio that it should run on, and the ID of the studio that it should search for commands in. Your username and password are only used for logging into Scratch. If you are worried about what it does with your information, you can read the source code. The ID of a studio is the unique number that identifies it. It can be found in the URL of the studio. For example, the studio ID of https://scratch.mit.edu/studios/146521/ is 146521. The studio and the command studio may be the same or different studios.

You should be good to go! The computer that it's running on must be on for the script to run, so if it falls asleep, the script will pause. You can set your computer to never go to sleep in your computer's settings. To stop the bot and return to the command line, press <kbd>Ctrl</kbd> + <kbd>C</kbd>.
