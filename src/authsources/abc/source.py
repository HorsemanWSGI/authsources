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
    __protocols__: t.Iterable[type[t.Protocol]]

    def __init__(self, source: "Source", request: RequestProtocol):
        self.source = source
        self.request = request


class Source(abc.ABC):
    title: str
    description: str
    usertype: type[User]
    _actions: dict[type[SourceAction], SourceAction]

    def get_action(
            self, type_: type[SourceAction], request: RequestProtocol):
        if (action := self._actions.get(type_)) is not None:
            return action(self, request)

    def define(self, actions: t.Iterable[type[SourceAction]]):
        defined = {}
        if actions:
            for action in actions:
                for protocol in action.__protocols__:
                    defined[protocol] = action
        self._actions = defined
