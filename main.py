import os
import sys
import argparse
from subscription_playlist import SubscriptionPlaylist

def get_subscription_dir():
    return os.path.join(os.path.dirname(__file__), 'subscriptions')

def get_subscription_file(name):
    return os.path.join(get_subscription_dir(), f'{name}.json')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--playlist', type=str, action='store', help='existing playlist')
    parser.add_argument('--add_channels', dest='channels', default=[], nargs="+", type=str, action='extend', help='add channel by name.  Does not update playlist')
    parser.add_argument('--update_all', action='store_true')

    args = parser.parse_args()

    if args.playlist:
        playlist_file = get_subscription_file(args.playlist)
        if os.path.exists(playlist_file):
            if args.channels:
                subscription_playlist = SubscriptionPlaylist(playlist_file)
                subscription_playlist.add_channels(args.channels)
        else:
            if args.channels:
                raise Exception(f"Playlist file not found: {playlist_file}")
            SubscriptionPlaylist.create_blank_playlist(playlist_file)
            
    if args.update_all:
        for basename in os.listdir(get_subscription_dir()):
            filename = os.path.join(get_subscription_dir(), basename)
            sp = SubscriptionPlaylist(filename)
            sp.update_playlist()
