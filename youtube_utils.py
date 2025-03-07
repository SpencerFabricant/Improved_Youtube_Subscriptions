# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from consts import get_settings

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_youtube():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    auth_token_file = get_settings().auth_token_file
    client_secrets_file = get_settings().client_secrets_file

    if os.path.exists(auth_token_file):
        creds = Credentials.from_authorized_user_file(auth_token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file(
              get_settings().client_secrets_file, SCOPES
          )
          creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(auth_token_file, "w") as token:
          token.write(creds.to_json())
          print(f'Credentials stored at {auth_token_file}')
    
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

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

def create_new_playlist(playlist_name):
    youtube = get_youtube()

    request = youtube.playlists().insert(
        part="snippet, status",
        body={
          "snippet": {
            "title": playlist_name,
            "defaultLanguage":"EN",
            "description":"test"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    response = request.execute()

    return response['id']

def add_video_to_playlist(playlist_id, video_id):
    youtube = get_youtube()

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlist_id,
            "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": video_id
            }
          }
        }
    )
    response = request.execute()
    


def main():
    after = '2024-06-01T00:00:00Z'
    channel_id = get_channel_id('jocat')
    print(get_video_ids_from_channel_id(channel_id, after=after))
    exit()


if __name__ == "__main__":
    main()
