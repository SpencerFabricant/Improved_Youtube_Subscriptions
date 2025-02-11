# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_youtube():
    api_key = os.environ['GOOGLE_API_KEY']
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key)
    
    return youtube

def get_channel_id(channel_name):
    youtube = get_youtube()

    request = youtube.channels().list(
            part="id",
            forHandle=channel_name
            )
    response = request.execute()
    
    return response['items'][0]['id']

def get_video_ids_from_channel_id(channel_id, after='1990-01-01T00:00:00Z', before='2990-01-01T00:00:00Z', page_token=''):
    youtube = get_youtube()

    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        order="date",
        publishedAfter=after,
        safeSearch="none",
        pageToken=page_token
    )
    response = request.execute()

    video_ids= [x['id']['videoId'] for x in response['items'] if 'id' in x and x['id']['kind'] == 'youtube#video']

    if 'nextPageToken' in response:
        next_page = response['nextPageToken']
        return video_ids + get_video_ids_from_channel_id(channel_id, after=after, before=before, page_token=next_page)

    return video_ids

def get_video_info(video_id):
    youtube = get_youtube()
    request = youtube.videos().list(
        part="player, contentDetails,snippet",
        id="TWFeHYvEMj4"
    )
    #TODO
    response = request.execute()


def get_now():
    return f'{datetime.utcnow().isoformat()}Z'

def main():
    after = '2024-06-01T00:00:00Z'
    channel_id = get_channel_id('jocat')
    print(get_video_ids_from_channel_id(channel_id, after=after))
    exit()


if __name__ == "__main__":
    main()
