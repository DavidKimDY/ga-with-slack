import json

from slack_sdk import WebClient


class SlackBot:
    def __init__(self):
        self.channel = '#httpscoretoday'
        token_dict =  self.get_token_json()
        token = token_dict['SLACK_BOT_TOKEN']
        token_priviate = token_dict['SLACK_BOT_TOKEN']
        self.client = WebClient(token=token)

    def get_token_json(self):
        with open('slack_api_key.json', 'r') as f:
            return json.load(f)

    def send_daily(self):
        self.client.files_upload(
            channels=self.channel,
            initial_comment='어제 하룻동안 각 게시물의 페이지뷰',
            file='daily_pageViews.png'
        )

    def send_weekly(self):
        self.client.files_upload(
            channels=self.channel,
            initial_comment='지난 한주간 각 게시물의 페이지뷰',
            file='weekly_pageViews.png'
        )

        self.client.files_upload(
            channels=self.channel,
            initial_comment='지난 한주간 유저들이 사용한 기기들의 비율',
            file='weekly_devices.png'
        )

