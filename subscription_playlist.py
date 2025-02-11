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
    def __init__(self, filename):
        """
        Load a subscription from 
        """

        self.subscription_filename = filename


        self.playlist_name = os.path.splitext(os.path.basename(filename))[0]
        if not os.path.isfile(self.subscription_filename):
            #TODO: Create a new file here
            raise Exception(f'Subscription not found at {subscription_dir}')
        
        with open(self.subscription_filename, 'rt') as f:
            self.subscription_data = json.load(f)

        self.validate_subscription_data()

        if 'playlist_id' in self.subscription_data:
            print("playlist id found")
            self.playlist_id = subscription_data['playlist_id']
        else:
            print("Creating new playlist")
            # The playlist has not been created.  Create one:
            self.playlist_id = youtube_utils.create_new_playlist(self.playlist_name)
            self.subscription_data['playlist_id'] = self.playlist_id
            self.save_subscription_data()


    def save_subscription_data(self):
        with open(self.subscription_filename, 'wt') as f:
            json.dump(self.subscription_data, f, indent=2)

    def save_video_data(self):
        with open(self.video_filename, 'wt') as f:
            json.dump(self.video_data, f, indent=2)

    def validate_subscription_data(self):
        updated = False
        for channel in self.subscription_data['channels']:
            if 'channel_id' not in channel and 'channel_name' not in channel:
                raise Exception('Expected "channel_name" in channel')

            if 'channel_id' not in channel:
                channel_id = youtube_utils.get_channel_id(channel['channel_name'])

                channel['channel_id'] = channel_id
                updated = True

            if 'last_fetch' not in channel:
                channel['last_fetch'] = get_init_subscription_time()

        if updated:
            self.save_subscription_data()

    def fetch_new_video_ids_and_update_playlist(self):
        new_videos = []
        for channel in self.subscription_data['channels']:
            now_timestamp = get_now()
            last_fetch = channel['last_fetch']
            channel_id = channel['channel_id']

            new_videos += youtube_utils.get_video_ids_from_channel_id(channel_id, after=last_fetch, before=now_timestamp)
            channel['last_fetch'] = now_timestamp


        for video_id in new_videos:
            print('adding {video_id}')
            youtube_utils.add_video_to_playlist(self.playlist_id, video_id)

        self.save_subscription_data()

        return new_videos

