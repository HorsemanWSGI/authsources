from typing import TypedDict, Iterable
from authsources.abc.source import Source
from authsources.abc.identity import User, UserID
from authsources.abc.source import SourceAction
from authsources.abc.actions import Challenge, Getter
from authsources.json import JSONSchema


class UserData(TypedDict, total=False):
    password: str


class DictUser(User):

    def __init__(self, id: UserID, data: UserData):
        self.id = id
        self.data = data


class Fetch(SourceAction):

    __protocols__ = (Getter,)

    schema = None

    def get(self, uid: UserID) -> User | None:
        if userdata := self.source.users.get(uid):
            return self.source.usertype(id=uid, data=userdata)


class Login(SourceAction):

    __protocols__ = (Challenge,)

    schema = JSONSchema({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Login",
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "description": "User name."
            },
            "password": {
                "type": "string",
                "description": "User password"
            }
        },
        "required": ["username", "password"]
    })

    def challenge(self, credentials: dict) -> User | None:
        errors = list(self.schema.validate(credentials))
        if not errors:
            username = credentials.get("username")
            password = credentials.get("password")
            if username is not None:
                if userdata := self.source.users.get(username):
                    if userdata['password'] == password:
                        return self.source.usertype(
                            id=username, data=userdata)
        else:
            # FixMe
            return None


class DictSource(Source):

    def __init__(self, users: dict[str, UserData], *,
                 title: str,
                 description: str,
                 usertype: type[DictUser] = DictUser,
                 actions: Iterable[SourceAction] | None = None):
        self.users = users
        self.title = title
        self.description = description
        self.usertype = usertype
        self.define(actions)
