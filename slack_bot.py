import json
import os

from slack_sdk import WebClient

class SlackBot:
    def __init__(self):
        self.channel = '#_test'
        token_dict =  self.get_token_json()
        token = token_dict['SLACK_BOT_TOKEN']
        token_priviate = token_dict['SLACK_BOT_TOKEN']
        self.client = WebClient(token=token)
    
    def make_path(self, file_path):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path)
        return path

    def get_token_json(self):
        with open(self.make_path('keys/slack_api_key.json'), 'r') as f:
            return json.load(f)

    def send_daily(self):
        self.client.files_upload(
            channels=self.channel,
            initial_comment='어제 하룻동안 각 게시물의 페이지뷰',
            file=self.make_path('daily_pageViews.png')
        )

    def send_weekly(self):
        self.client.files_upload(
            channels=self.channel,
            initial_comment='지난 한주간 각 게시물의 페이지뷰',
            file=self.make_path('weekly_pageViews.png')
        )

        self.client.files_upload(
            channels=self.channel,
            initial_comment='지난 한주간 유저들이 사용한 기기들의 비율',
            file=self.make_path('weekly_devices.png')
        )

