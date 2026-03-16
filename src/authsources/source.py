import abc
import typing as t
from copy import copy
from authsources.identity import User, UserID
from authsources.json import JSONSchema


class SourceAction:
    __protocols__: t.ClassVar[t.Iterable[type[t.Protocol]]]

    source: 'Source'
    schema: JSONSchema | None = None

    def __init__(self, source: "Source"):
        self.source = source


class Source:
    title: str
    description: str
    usertype: type[User]
    _actions: dict[type[SourceAction], SourceAction]

    def __init__(self, *,
                 title,
                 description,
                 usertype,
                 actions: t.Iterable[SourceAction] | None = None,
                 bindings: t.Mapping | None = None
                 ):
        self.title = title
        self.description = description
        self.usertype = usertype
        self.bindings = bindings if bindings is not None else {}
        self.define(actions)

    def get(self, type_: type[SourceAction]):
        if (action := self._actions.get(type_)) is not None:
            return action(self)

    def __getitem__(self, type_: type[SourceAction]) -> SourceAction:
        action = self._actions[type_]
        return action(self)

    def __contains__(self, type_: type[SourceAction]) -> bool:
        return type_ in self._actions

    def define(self, actions: t.Iterable[type[SourceAction]]):
        defined = {}
        if actions:
            for action in actions:
                for protocol in action.__protocols__:
                    defined[protocol] = action
        self._actions = defined

    def bind(self, **bindings):
        bound = copy(self)
        bound.bindings = {**bound.bindings, **bindings}
        return bound
