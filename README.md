# PRIZM
My first ever bot, PRIZM ;]

> This repo is not updated very often, only big changes such as completely new code will be 
pushed weekly

# What is PRIZM?
PRIZM is a Discord bot that honestly has too many features. It can interact with Reddit, 
play games with you, be your math assistant, be your personal radio, and so much more.

## INSTALL STUFF
### Download PRIZM -----
Download this entire repo as a zip, then make sure that all the following commands are done 
inside of the `bot` folder, where you can see `PRIZM.py`

### Dependencies -----
**USE PYTHON 3.7**, Python 3.8 doesn't work with TensorFlow and most other modules that I need
for this bot to work.

**USE LINUX**, preferably some form of Ubuntu if you want to use TensorFlow.

**CHECK THE /bot/avx/avx FILE** to see if your **Intel** CPU supports AVX [for TensorFlow],
if you have a Ryzen CPU, you are most likely fine.

Use `pip3 install -r req.txt` to install all the requirements and depndencies except for 
`libffmpeg`, that is an app.
This will take several minutes to install because there are like 200 modules [more like 10 
but ok]

You must also install `ffmpeg` to actually play music and to convert stuff, it is not a 
library, but an app you need to install.

For debian users ] `sudo apt install ffmpeg -y`

In order to use the `;]mix` command, you must also download [this file](https://mega.nz/#!9fh1iQzC!5d9zt6yKRbAXzgyxNMmoITua09b__zlU751KKOfpRSs)
and place it in the `mix` folder [~500mb], and you must have linux because
TensorFlow won't actually install on windows from my experience
> I will fix some issues with TensorFlow in light of version 2 coming out shortly

If you have issues installing the requirements, get `pip` first.
> For Debian users ] `sudo apt install python3-pip`

If you still have trouble, then idk whats happening.

## RUN PRIZM ;]
When all your dependencies are finished, do `python3.7 PRIZM.py`, or whatever other `pythonX` 
prefix you have

PRIZM is meant to be faily verbose, it logs whenever an error occurs and when other things 
regarding how the bot acts when it happens.

## EMOJI AND ASCIIMOJI
This bot uses custom emojis. To gain access to these emojis please send the invite link in
the `#bot-invite-links` channel in the [emojis guild](https://discord.gg/eYMyfcd). If you
want these emojis, just join the guild.

## Other notes
If you are editing the bot, do **NOT** change the support server link, but instead add it
by adding the following line to the end of the links of the `;]inv` command. Not doing so may
result in improper help or info whenever somebody asks for it.
```
 // [Second Support Option](<guild invite>)
```

Do **NOT** change the `;]bug` command channel, but instead copy and paste the line [make sure 
indentation is correct] and place the new channel in there.
