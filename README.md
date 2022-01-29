# What is this

Non-technical:<br>
This is a Python script to share the top left corner of your screen with the kindle without having to jailbreak it.

More technical:<br>
This is a Python script that starts a webserver, that provides a page, which mirrors the top left corner of the computer screen it's running on. It allows only one single client to connect.

# How to use
- On Computer:
  - Download script
  - Install all dependencies (see below)
  - `python3 emonitor.py`
  -  Notice, that you be told what to enter into your kindle
- On Kindle:
  - Open browser
  - Type in what the computer told you to enter

# Dependencies

- Python3
- Gtk
  - Windows: `python3 -m pip install pygtk` (?)
  - Ubuntu: `sudo apt install python3 python3-gi` (?)
- Kindle and computer must be on the same network

# Security

None.

The mirroring (connection) between Kindle and computer is not encrypted. Anyone intercepting the traffic would be able to also see the content.
