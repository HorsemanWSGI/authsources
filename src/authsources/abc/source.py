import abc
import typing as t
from authsources.abc.identity import User, UserID
from authsources.json import JSONSchema
from wrapt import ObjectProxy


class SourceAction:
    source: 'Source'
    schema: JSONSchema | None
    __protocols__: t.ClassVar[t.Iterable[type[t.Protocol]]]

    def __init__(self, source: "Source"):
        self.source = source


class BoundSource(ObjectProxy):
    bindings: dict

    def __init__(self, wrapped: "Source", bindings: dict):
        super().__init__(wrapped)
        self.bindings = bindings


class Source(abc.ABC):
    title: str
    description: str
    usertype: type[User]
    _actions: dict[type[SourceAction], SourceAction]

    @property
    def bindings(self):
        raise RuntimeError("Source is currently unbound")

    def get(self, type_: type[SourceAction]):
        if (action := self._actions.get(type_)) is not None:
            return action(self)

    def __getitem__(self, type_: type[SourceAction]):
        action = self._actions[type_]
        return action(self)

    def define(self, actions: t.Iterable[type[SourceAction]]):
        defined = {}
        if actions:
            for action in actions:
                for protocol in action.__protocols__:
                    defined[protocol] = action
        self._actions = defined

    def bind(self, **bindings):
        return BoundSource(self, bindings)
