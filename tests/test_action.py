import pytest
from typing import Protocol
from authsources.abc.identity import User
from authsources.abc.source import SourceAction, Source


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


def test_source():
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

    bound = source.bind(person="Thomas")
    assert source is not bound
    action = bound.get(MyOtherProtocol)
    assert action.something_else() == "Thomas"
