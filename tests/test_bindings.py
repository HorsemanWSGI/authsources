import pytest
from typing import Protocol
from authsources.identity import User
from authsources.source import SourceAction, Source


class MyUser(User):

    def __init__(self, userid: str, data: dict | None = None):
        self.userid = userid
        self.data = data if data is not None else {}


class MyProtocol(Protocol):

    def test(self):
        pass


class MyTestSourceAction(SourceAction):
    __protocols__ = (MyProtocol,)

    def test(self):
        return self.source.bindings['person']


def test_source_bindings():
    source = Source(
        title="test",
        description="Test source",
        usertype=MyUser,
        actions=(MyTestSourceAction,)
    )
    bound = source.bind(person="Thomas")
    assert source is not bound

    action = bound.get(MyProtocol)
    assert action.test() == "Thomas"
