import os
import sys
import argparse
from subscription_playlist import SubscriptionPlaylist

SUBSCRIPTION_DIR = os.path.join(os.path.dirname(__file__), 'subscriptions')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--playlist', type=str, action='store', help='existing playlist')
    parser.add_argument('--add_channel', type=str, action='store', help='add channel by name.  Does not update playlist')
    parser.add_argument('--update_all', action='store_true')

    class Args:
        pass

    args = Args()
    parser.parse_args(namespace=args)
    print(args.playlist)
