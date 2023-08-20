import json
import os

from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id: str):
        self.__video_id = video_id  # id видео;
        video_response = youtube.videos().list(id=self.__video_id,
                                               part='snippet,statistics,contentDetails,topicDetails').execute()
        self.video_title = video_response['items'][0]['snippet']['title']  # Название видео
        self.url = 'https://youtu.be/' + video_id  # Ссылка на видео
        self.view_count = video_response['items'][0]['statistics']['viewCount']  # Кол-во просмотров
        self.count_likes = video_response['items'][0]['statistics']['likeCount']  # Кол-во лайков


class PLVideo:
    def __init__(self, video_id: str, playlist_id: str):
        self.__video_id = video_id  # id видео;
        video_response = youtube.videos().list(id=self.__video_id,
                                               part='snippet,statistics,contentDetails,topicDetails').execute()
        # playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
        #                                      part='contentDetails', maxResults=50,).execute()
        # print(playlist_videos)
        self.video_title = video_response['items'][0]['snippet']['title']  # Название видео
        self.url = 'https://youtu.be/' + playlist_id + '/' + video_id  # Ссылка на видео
        self.view_count = video_response['items'][0]['statistics']['viewCount']  # Кол-во просмотров
        self.count_likes = video_response['items'][0]['statistics']['likeCount']  # Кол-во лайков
        self.__playlist_id = playlist_id
