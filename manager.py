from mappings import users
from classes import Client


class Manager:
    users = dict()

    @classmethod
    def register_user(cls):
        new_uuid = Client.get_next_guid()
        users[new_uuid] = Client(new_uuid)
        return new_uuid
