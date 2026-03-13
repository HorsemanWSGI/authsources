import abc
import uuid


UserID = str | int | uuid.UUID


class User(abc.ABC):
    id: UserID
