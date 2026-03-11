import abc
import typing as t
from authsources.abc.identity import User, UserID
from authsources.json import JSONSchema


class RequestProtocol(t.Protocol):
    pass


class SourceAction:
    schema: JSONSchema | None
    source: 'Source'
    request: RequestProtocol

    def __init__(self, source: "Source", request: RequestProtocol):
        self.source = source
        self.request = request


class Source(abc.ABC):
    title: str
    description: str
    actions: dict[type[SourceAction], SourceAction]
    usertype: t.Type[User]

    def get_action(
            self, type_: type[SourceAction], request: RequestProtocol):
        if (action := self.actions.get(type_)) is not None:
            return action(self, request)
