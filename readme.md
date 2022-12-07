# Amis invisible

This package is based on [telethon](https://github.com/LonamiWebs/Telethon) package and people who love play board games
to play a game call invisible friends.  
The principle is easy. we group of friends where each one must give a present to another one and must receive a present
from someone. The receiver is not suppose to know from who the gift is coming.  
So to allow every body to participate. I have automate this process by :

1. Scraping members from Telegram group.
2. Mixing these members in order to make pairs
3. Sending Automate message to each member.
4. Send the final list to someone.

# Installation

You must have python >=3.10 installed

## Create a virtual environment

`python -m venv your_virtual_env_name`

## Requirements

`pip install -r requirements.txt`

# Setup

1. Create an Apps on [telegram.org](https://my.telegram.org/auth)
2. Provide your credential in .env file
3. You can provide a different message in AmisInvisible class located in amis_invisibles.py
4. The job is done

# run

`python main.py`
