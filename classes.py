from datetime import datetime
import uuid
import json
from random import choice


class Client:
    guid = None
    mailbox = None
    background = None
    user = None
    environment = None
    history = None

    @classmethod
    def get_next_guid(cls):
        return str(uuid.uuid4())

    def __init__(self, guid):
        self.guid = guid
        self.mailbox = MailBox()
        self.background = UserBackground(None, None, None, None)
        self.environment = Environment()
        self.user = User()
        self.history = History()

    def responce(self):
        return {
            "rating": self.user.rating,
            "money": self.user.money,
            "env": self.environment.response(),
            "news": NewsList.get_last().response(),
            "events": {
                "mails": self.mailbox.get_new_mails_count(),
                "network": 0,
                "devices": 0,
                "software": 0,
            }
        }


class MailBox:
    mails = {}
    new = []
    archive = []

    def __init__(self):
        pass

    def add_new(self, mail):
        self.new.append(mail)
        self.mails[mail.id] = mail

    def mail_processed(self, mail_id):
        mail = self.mails[mail_id]
        self.new.remove(mail)
        self.archive.append(mail)

    def get_new_mails(self):
        return self.new

    def get_new_mails_count(self):
        return len(self.new)

    def responce(self):
        response = []
        for mail in self.get_new_mails():
            response.append(mail.response())
        return {"mails": response}


class UserBackground:
    boss = 'начальник'
    bssid = 'TPLink 0707'
    email = ''
    ldap = 'office'

    def __init__(self, boss, bssid, email, ldap):
        if boss:
            self.boss = boss
        if bssid:
            self.bssid = bssid
        if ldap:
            self.ldap = ldap
        if email:
            self.email = email
        else:
            self.email = self.ldap + '@mail.ru'

    def form_mail_from(self, address_type):
        if address_type == 'начальник':
            return self.boss

    def form_mail_to(self, address_type):
        if not address_type:
            return self.email


class Mail:
    counter = 0

    id = None
    header = ''
    attachments = []
    text = ''
    sent = ''
    received = ''
    date = None
    actions = []

    @classmethod
    def get_id(cls):
        cls.counter += 1
        return cls.counter

    def __init__(self, header, attachments, text, sent, date, actions, receiver):
        self.id = Mail.get_id()
        self.header = header
        self.attachments = attachments
        self.text = text
        # self.sent = UserBackground.form_mail_from(sent)
        self.sent = sent
        if not date:
            self.date = datetime.now()
        # self.receiver = UserBackground.form_mail_to(receiver)
        self.receiver = receiver

        self.actions = []
        for i, action in enumerate(actions):
            action['id'] = i
            self.actions.append(Action(
                i,
                action['text'],
                action['correct'],
                action['rating'],
                action['environment'],
                action['answer'],
                ''
            ))

    def perform_action(self, action_id, client):
        responce = self.actions[action_id].perform(client)
        client.mailbox.mail_processed(self.id)
        return responce

    def response(self):
        actions = []
        for action in self.actions:
            actions.append(action.response())
        return {
            "id": self.id,
            "header": self.header,
            "text": self.text,
            "sent": self.sent,
            "receiver": self.receiver,
            "date": self.date,
            "attachments": self.attachments,
            "actions": actions,
        }


class Action:
    id = 0
    feedback = None

    text = ''
    correct = True
    rating = 0
    environment = 0
    answer = ''

    def __init__(self, id, text, correct, rating, environment, answer, link):
        self.id = id
        self.text = text
        self.correct = correct
        self.rating = rating
        self.environment = environment
        self.answer = answer
        self.link = link
        self.feedback = Feedback(correct, answer, link)

    def perform(self, client):
        client.user.add_rating(self.rating)
        client.environment.add_scores(self.environment)
        return self.feedback.response()

    def response(self):
        return {
            "id": self.id,
            "text": self.text,
        }


class Feedback:
    correct = True
    text = 'OK'
    link = ''

    def __init__(self, correct, text, link):
        self.correct = correct
        self.text = text
        self.link = link

    def response(self):
        return {
            "result": self.correct,
            "feedback": {
                "text": self.text,
                "link": self.link,
            }
        }


class User:
    money = 4000
    last_salary = None
    statuses = (
        {
            'name': 'Ламер',
            'salary': 1000,
            'next level': 16,
        }, {
            'name': 'Уверенный пользователь',
            'salary': 1000,
            'next level': 10,
        }, {
            'name': 'Эникей',
            'salary': 1000,
            'next level': 50,
        }, {
            'name': 'Админ',
            'salary': 1000,
            'next level': 200,
        }, {
            'name': 'Хакер',
            'salary': 1000,
            'next level': 1000000,
        },
    )
    status = statuses[0]
    rating = 4
    name = 'Василий П.'

    def __init__(self):
        self.last_salary = datetime.now()
        self.rating = 14
        self.status = User.statuses[0]
        self.money = 4000

    def salary(self):
        self.money += self.status['salary']
        self.last_salary = datetime.now()

    def add_rating(self, rating):
        self.rating += rating
        if self.rating >= self.status['next level']:
            self.status = User.statuses[
                User.statuses.index(self.status) + 1
                ]

    def purchase(self, cost):
        if self.money - cost >= 0:
            self.money -= cost
        else:
            from exceptions import NotEnoughtMoney
            raise NotEnoughtMoney()


class Environment:
    states = [
        {
            'state': 0,
            'cpu': 20,
            'ram': 1000,
            'network': 100,
            'scores': 45,
        }, {
            'state': 1,
            'cpu': 45,
            'ram': 2500,
            'network': 135,
            'scores': 20,
        }, {
            'state': 2,
            'cpu': 80,
            'ram': 3800,
            'network': 350,
            'scores': 0,
        }
    ]

    scores = 0
    last_av_check = None
    state = states[0]

    def __init__(self):
        self.last_av_check = datetime.now()
        self.scores = 50
        self.state = Environment.states[0]

    def add_scores(self, scores):
        self.scores += scores
        index = self.state['state']
        if index < len(Environment.states) - 1:
            if self.scores <= Environment.states[index + 1]['scores']:
                self.state = Environment.states[index + 1]
        if index > 0:
            if self.scores > Environment.states[index - 1]['scores']:
                self.state = Environment.states[index - 1]

    def av_checked(self):
        self.last_av_check = datetime.now()

    def adminated(self):
        self.state = Environment.states[0]
        self.scores = 50
        self.av_checked()

    def response(self):
        return {
            "state": self.state['state'],
            "cpu": self.state['cpu'],
            "ram": self.state['ram'],
            "network": self.state['network'],
            "lastAvCheck": str(self.last_av_check),
        }


class History:
    events = []

    def add(self, header, body, event_type, result):
        self.events.append((header, body, event_type, result))

    def response(self):
        pass


class Rating:
    pass


class NewsList:
    news = []

    @classmethod
    def set_hot_news(cls, news):
        cls.news = [news]
        # it's a dummy!

    @classmethod
    def add_news(cls, news):
        cls.news.append(news)

    @classmethod
    def get_last(cls):
        return choice(cls.news)
    # it's a dummy too!


class News:
    tag = None
    text = None
    link = None

    def __init__(self, tag, text, link):
        self.tag = tag
        self.text = text
        self.link = link

    def response(self):
        return {
            "tag": self.tag,
            "text": self.text,
            "link": self.link,
        }


class Buff:
    name = ""
    cost = 0
    description = ""
    id = 0

    @classmethod
    def action(cls, client):
        pass


class BetterCallAdmin(Buff):
    name = "Позвать сисадмина"
    cost = 500
    description = "Позвонить Диме Каданцеву. Вы точно этого хотите?"
    id = 1

    @classmethod
    def action(cls, client):
        client.environment.adminated()
        client.user.purchase(cls.cost)


class Offense:
    name = ""
    cost = 0
    description = ""
    id = 100

    @classmethod
    def action(cls, client):
        pass


class SpamEverywhere(Offense):
    name = "Заказать спам"
    cost = 2000
    description = "Заказать спам на всех игроков, кроме себя. Вам срочно нужно продать самогонный аппарат?"
    id = 101

    @classmethod
    def action(cls, client):
        client.user.purchase(cls.cost)


class Shop:
    buffs = [
        BetterCallAdmin,
    ]
    offenses = [
        SpamEverywhere,
    ]

    @classmethod
    def response(cls):
        buffs_offers = []
        for buff in cls.buffs:
            buffs_offers.append({
                "name": buff.name,
                "cost": buff.cost,
                "description": buff.description,
                "id": buff.id,
            })

        offenses_offers = []
        for offense in cls.offenses:
            offenses_offers.append({
                "name": offense.name,
                "cost": offense.cost,
                "description": offense.description,
                "id": offense.id,
            })

        return {
            "buff": buffs_offers,
            "attack": offenses_offers,
        }
