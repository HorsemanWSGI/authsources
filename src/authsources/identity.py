import abc
import uuid
from typing import Mapping


UserID = str | int | uuid.UUID


class User(abc.ABC):
    id: UserID
    data: Mapping | None
