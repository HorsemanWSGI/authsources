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


class MyOtherProtocol(Protocol):

    def something_else(self):
        pass


class MyTestSourceAction(SourceAction):
    __protocols__ = (MyProtocol, MyOtherProtocol)

    def test(self):
        return "test"

    def something_else(self):
        return self.source.bindings['person']


class MySource(Source):
    pass


def test_source_no_actions():
    source = MySource(
        title="test",
        description="Test source",
        usertype=MyUser
    )
    assert list(source) == []


def test_source_action_multi_protocols():
    source = MySource(
        title="test",
        description="Test source",
        usertype=MyUser,
        actions=(MyTestSourceAction,)
    )
    action = source.get(MyProtocol)
    assert isinstance(action, MyTestSourceAction)
    assert action.test() == 'test'

    action = source.get(MyOtherProtocol)
    assert isinstance(action, MyTestSourceAction)
    with pytest.raises(KeyError):
        action.something_else()

    assert list(source) == [MyProtocol, MyOtherProtocol]
