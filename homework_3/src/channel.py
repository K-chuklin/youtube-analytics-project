import json
import os


from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:

    def __init__(self, channel_id: str, ) -> None:
        self.__channel_id = channel_id

        channel_id = self.__channel_id
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/' + channel['items'][0]['snippet']['customUrl']
        self.subscribers_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return f'{int(self.subscribers_count) + int(other.subscribers_count)}'

    def __sub__(self, other):
        return f'{int(self.subscribers_count) - int(other.subscribers_count)}'

    def __gt__(self, other):
        if int(self.subscribers_count) > int(other.subscribers_count):
            return True
        else:
            return False

    def __ge__(self, other):
        if int(self.subscribers_count) >= int(other.subscribers_count):
            return True
        else:
            return False

    def __lt__(self, other):
        if int(self.subscribers_count) < int(other.subscribers_count):
            return True
        else:
            return False

    def __le__(self, other):
        if int(self.subscribers_count) <= int(other.subscribers_count):
            return True
        else:
            return False

    def __eq__(self, other):
        if int(self.subscribers_count) == int(other.subscribers_count):
            return True
        else:
            return False

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file):
        with open(file, 'wt') as file:
            data = {'chanel_id': self.__channel_id,
                    'title': self.title,
                    'description': self.description,
                    'url': self.url,
                    'subscribers_count': self.subscribers_count,
                    'video_count': self.video_count,
                    'view_count': self.view_count}
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            file.write(json_data)
