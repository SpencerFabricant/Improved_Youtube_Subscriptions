#!/usr/bin/python3

import os
import sys
import argparse
from subscription_playlist import SubscriptionPlaylist
from consts import reset_settings_to_default, get_settings
import youtube_utils

def get_subscription_file(name):
    return os.path.join(get_settings().subscriptions_dir, f'{name}.json')

def get_all_subcription_files():
    files = []
    for basename in os.listdir(get_settings().subscriptions_dir):
        files.append(os.path.join(get_settings().subscriptions_dir, basename))
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--new_playlist', type=str, action='store')

    parser.add_argument('--playlist', type=str, action='store')
    parser.add_argument('--add_channels', dest='channels', default=[], nargs="+", type=str, action='extend', help='add channel by name.  Does not update playlist.  Requires a valid --playlist')
    parser.add_argument('--update_all', action='store_true', help=f'Update all of the subscription playlists in {get_settings().subscriptions_dir}/')
    parser.add_argument('--reset_settings_to_default', action='store_true')

    parser.add_argument('--update_token', action='store_true')

    parser.add_argument('--list_subscriptions', action='store_true')

    args = parser.parse_args()

    # init the settings file no matter what
    get_settings()

    if args.update_token:
        os.remove(get_settings().auth_token_file)
        youtube_utils.get_youtube()
        exit()

    if args.reset_settings_to_default:
        reset_settings_to_default()
        print(f"Settings reset.  To modify, edit {os.path.join(os.getcwd(), 'settings')}")
    elif args.list_subscriptions:
        for filename in get_all_subcription_files():
            SubscriptionPlaylist(filename).print()
            print()

    elif args.new_playlist:
        new_playlist_file = get_subscription_file(args.new_playlist)
        SubscriptionPlaylist.create_blank_playlist(playlist_file)
    elif args.playlist:
        playlist_file = get_subscription_file(args.playlist)
        if os.path.exists(playlist_file):
            if args.channels:
                subscription_playlist = SubscriptionPlaylist(playlist_file)
                subscription_playlist.add_channels(args.channels)
            else:
                raise Exception("--playlist requires --new_channels.  Exiting...")
        else:
            raise Exception(f"Playlist file not found: {playlist_file}")
            
    elif args.update_all:
        for filename in get_all_subcription_files():
            sp = SubscriptionPlaylist(filename)
            sp.update_playlist()
    else:
        parser.print_help()
