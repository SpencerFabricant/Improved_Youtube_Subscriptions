# Improved YouTube Subscriptions

## Motivation
There are a number of artisan creators that I like, but finding their videos in the mess of all of my other subscriptions is a mess.  I wanted a way to have all of those videos in one place.  YouTube's algorithmically-generated content feed is no good for this.


I wanted there to be a way to have playlists on YouTube that automatically subscribe to specific channels, and there is no built-in way to do this.


## Installation Steps
To install the dependencies, run `pip3 install -r requirements.py`
To use this software, you will need to obtain [Google OAuth 2.0 credentials](https://developers.google.com/identity/protocols/oauth2).
Running this software will create a `settings` file.  Set `client_secrets_file` to your OAuth2.0 credentials json file.


## Usage
```
usage: ./main.py [-h] [--new_playlist NEW_PLAYLIST] [--playlist PLAYLIST]
               [--add_channels CHANNELS [CHANNELS ...]] [--update_all]
               [--reset_settings_to_default] [--list_subscriptions]

options:
  -h, --help            show this help message and exit
  --new_playlist NEW_PLAYLIST
  --playlist PLAYLIST
  --add_channels CHANNELS [CHANNELS ...]
                        add channel by name. Does not update playlist. Requires a valid --playlist

  --update_all          Update all of the subscription playlists in subscriptions/
  --reset_settings_to_default
  --list_subscriptions
```
The first time you run this, it will create the settings file.
To create a playlist, run `python3 main.py --new_playlist [playlist_name]`
Then to add channels to that playlist: `python3 main.py --playlist [playlist_name] --add_channels [channel1] [channel2]... [channel_99]`
To have the playlists be created or updated on your youtube account, run `python3 main.py --update_all`
I would recommend having this last command run as a cron job. Adding the following line to `crontab -e` will update the playlists 3 times a day:
```
0 1,12,19 * * * python3 /path/to/directory/main.py --update_all
```
