import json
import os
from os import path

import utils


SUBSCRIPTION_JSON = 'subscription.json'
VIDEOS_JSON = 'videos.json'

class Subscription:
    def __init__(self, subscription_dir):
        """
        Load a subscription from <subscription_dir>
        """
        self.subscription_filename = path.join(subscription_dir, SUBSCRIPTION_JSON)
        self.video_filename = path.join(subscrpition_dir, VIDEOS_JSON)

        if not path.isdir(subscription_dir) or not path.isfile(self.subscription_filename):
            raise Exception(f'Subscription not found at {subscription_dir}')
        
        with open(self.subscription_filename, 'rt') as f:
            self.subscription_data = json.load(f)

        with open(self.video_filename, 'rt') as f:
            self.video_data = json.load(f)

        self.validate_subscription_data()


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
                channel_id = utils.get_channel_id(channel['channel_name'])

                channel['channel_id'] = channel_id
                updated = True

            if 'last_fetch' not in channel:
                channel['last_fetch'] = utils.get_now()

        if updated:
            self.save_subscription_data()

    def fetch_video_ids(self, save=False):
        for channel in self.subscription_data['channels']:
            now_timestamp = utils.get_now()
            last_fetch = channel['last_fetch']

            new_videos = utils.get_video_ids_from_channel_id(channel_id, after=last_fetch, before=now_timestamp)
            channel['last_fetch'] = new_timestamp

            for video_id in new_video:
                video = utils.get_video_info(video_id)
        
        if save:
            save_video_data()
            save_subscription_data()
