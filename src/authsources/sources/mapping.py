from authsources.abc.source import Source
from authsources.abc.identity import User, UserID
from authsources.abc.actions import Challenge, Getter
from authsources.json import JSONSchema


class DictUser(User):

    def __init__(self, id: UserId):
        self.id = id


class Fetch(Getter):

    schema = None

    def get(self, uid: UserID) -> User | None:
        if uid in self.source.users:
            return self.source.usertype(id=username)


class Login(Challenge):

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
            if username is not None and username in self.source.users:
                if self.source.users[username] == password:
                    return self.source.usertype(id=username)
        else:
            # FixMe
            return None


class DictSource(Source):

    actions = {
        Challenge: Login
    }

    def __init__(self, users: dict[str, str], *,
                 title: str,
                 description: str,
                 usertype: t.Type[DictUser] = DictUser):
        self.users = users
        self.title = title
        self.description = description
        self.usertype = usertype
