from enum import Enum
import json

from classes import Mail, News, NewsList
from mappings import users


class Selection(Enum):
    RANDOM = 0
    FIRST = 1
    LAST = 2


class MailingService:
    mails = []

    @classmethod
    def get_next(cls):
        return cls.mails.pop()

    @classmethod
    def add_mail(cls, mail):
        cls.mails.append(mail)

    @classmethod
    def make_broadcast(cls, mail):
        for client in users.values():
            client.mailbox.add_new(Mail(**mail))


class Scenario:
    mail_file = 'mails.json'

    @classmethod
    def test_curcit(cls):
        with open("mails.json", "r", encoding='utf8') as mails_json:
            mails_list = json.load(mails_json)

        for mail in mails_list['root']:
            MailingService.make_broadcast(mail)

        with open("news.json", "r", encoding='utf8') as news_json:
            news_list = json.load(news_json)
            for news in news_list['root']:
                NewsList.add_news(News(**news))
