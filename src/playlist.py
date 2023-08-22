from googleapiclient.discovery import build
from datetime import timedelta
from typing import List
import isodate
import os

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, channel_id: str):
        self.__total = None
        self.channel_id = channel_id
        channel_id = self.channel_id
        playlists = youtube.playlists().list(id=channel_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()

        self.title = playlists['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + channel_id

    @property
    def total_duration(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.channel_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: List[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        self.__total = timedelta(hours=0)
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_duration)
            self.__total += duration
        return self.__total

    def show_best_video(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.channel_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: List[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        '''
        Создем переменные:  
            - best_video - для сравнения и перезписи, в нее видео с нибольшим likeCount
            - best_video_id - для хранения в ней id видео с наибольшим likeCount
        '''
        best_video = 0
        best_video_id = ""
        for video in video_response['items']:
            new_video = int(video['statistics']['likeCount'])
            if best_video < new_video:
                best_video = new_video
                best_video_id = video['id']

        return "https://youtu.be/" + best_video_id

    def __str__(self):
        return self.__total
