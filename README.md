# PRIZM
My first ever bot, PRIZM ;]

> This repo is not updated very often

# What is PRIZM?
PRIZM is a Discord bot that honestly has too many features. It can interact with Reddit,
play games with you, be your math assistant, be your personal radio, and so much more.

## INSTALL STUFF
### NOTICE
PRIZM can only run on Linux, due to Linux's `git` and other terminal integrations.

### Download PRIZM -----
Download this entire repo as a zip, then make sure that all the following commands are done
inside of the `bot` folder, where you can see `PRIZM.py`

### Single command install for PRIZM
Open the terminal and cd into your `bot` folder where `PRIZM.py` is located, the run the following
command

`sudo apt install ffmpeg -y && sudo apt install python3.7 && python3.7 -m pip install -r req.txt`

Sit back and relax for a couple minutes

### Build Yourself
#### Installation notes
**USE PYTHON 3.7.X**, Python 3.8 has several issues with installing the dependencies, here is a small list of
what it refuses to install:
```
TensorFlow #This is on TensorFlow's end, they don't allow it.
```

**NOTE:** If you are planning on using the image mix command, make sure you use `Ubuntu`,
`Kubuntu`, `Lubuntu`, or `Xubuntu`. Also check to see if your CPU supports AVX.
- If you have a Zen based CPU [eg Ryzen] then you are most likely fine
- If you have an Intel CPU, use `sudo lshw | grep -e avx`, if anything shows then you are good

#### Dependencies -----

Use `pip3 install -r req.txt` to install all the requirements for python itself.
Then run `sudo apt install ffmpeg -y` to have the conversion technology and music abilities.

> `sudo apt install` is for Debian, your command may very

You must also download [this file]
(https://mega.nz/#!9fh1iQzC!5d9zt6yKRbAXzgyxNMmoITua09b__zlU751KKOfpRSs)
and place it in the `mix` folder [~500mb]
> I will fix some issues with TensorFlow in light of version 2 coming out shortly

If you have issues installing the python requirements, get `pip` first.
> For Debian users ] `sudo apt install python3-pip`

If you still have trouble, then idk whats happening.

## RUN PRIZM ;]
When all your dependencies are finished, do `python3.7 PRIZM.py`, or whatever other `pythonX`
prefix you have

PRIZM is meant to be fairly verbose, it logs whenever an error occurs and when other things
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
