import json
import os
import sys
import argparse

import youtube_utils
from datetime import datetime, timedelta


# when adding a channel to a subscription, include videos made up to 14 days earlier
SUBSCRIPTION_OFFSET_DAYS = 14


def get_now():
    return f'{datetime.utcnow().isoformat()}Z'

def get_init_subscription_time():
    start_time = datetime.utcnow() - timedelta(days=SUBSCRIPTION_OFFSET_DAYS)
    return f'{start_time.isoformat()}Z'


class SubscriptionPlaylist:
    @classmethod
    def create_blank_playlist(cls, filename):
        if os.path.exists(filename):
            raise Exception(f"Attempted to create subscription file where one already exists: {filename}")
        blank_playlist = { "channels": [] }
        with open(filename, 'wt') as f:
            json.dump(blank_playlist, f, indent=2)


    def __init__(self, filename, create_new_file=False):
        """
        Load a subscription from 
        """

        self.subscription_filename = filename

        self.playlist_name = os.path.splitext(os.path.basename(filename))[0]
        if not os.path.isfile(self.subscription_filename):
            raise Exception(f'Subscription not found at {subscription_dir}')
        
        with open(self.subscription_filename, 'rt') as f:
            self.data = json.load(f)

        self._validate()


    def _save_data(self):
        with open(self.subscription_filename, 'wt') as f:
            json.dump(self.data, f, indent=2)


    def _validate(self):
        updated = False
        for channel in self.data['channels']:
            if 'channel_id' not in channel and 'channel_name' not in channel:
                raise Exception('Expected "channel_name" in channel')

            if 'channel_id' not in channel:
                channel_id = youtube_utils.get_channel_id(channel['channel_name'])

                channel['channel_id'] = channel_id
                updated = True

            if 'last_fetch' not in channel:
                channel['last_fetch'] = get_init_subscription_time()
                updated = True

        if updated:
            self._save_data()

    def update_playlist(self):
        playlist_id = ''
        if 'playlist_id' in self.data:
            print("playlist id found")
            playlist_id = self.data['playlist_id']
        else:
            print("Creating new playlist")
            # The playlist has not been created.  Create one:
            playlist_id = youtube_utils.create_new_playlist(self.playlist_name)
            self.data['playlist_id'] = playlist_id
            self._save_data()

        new_videos = []
        for channel in self.data['channels']:
            now_timestamp = get_now()
            last_fetch = channel['last_fetch']
            channel_id = channel['channel_id']

            new_videos += youtube_utils.get_video_ids_from_channel_id(channel_id, after=last_fetch, before=now_timestamp)
            channel['last_fetch'] = now_timestamp


        for video_id in new_videos:
            print('adding {video_id}')
            youtube_utils.add_video_to_playlist(playlist_id, video_id)

        self._save_data()

        return new_videos

    def add_channels(self, channel_names):
        for channel_name in channel_names:
            self.data['channels'].append( {
                "channel_name": channel_name,
                "last_fetch": get_init_subscription_time()
                } )
        self._save_data()
