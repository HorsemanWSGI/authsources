from authsources.sources.mapping import DictSource, DictUser, Login
from authsources import protocols


def test_dict_source_base():
    source = DictSource(
        users={
            "test": {
                "password": "test"
            },
        },
        title="test",
        description="Test of DictSource",
    )
    assert source.users == {
        "test": {
            "password": "test"
        },
    }
    assert source.usertype is DictUser


def test_dict_source_bindings():
    source = DictSource(
        users={
            "test": {
                "password": "test"
            },
        },
        title="test",
        description="Test of DictSource",
    )
    assert source.bindings == {}

    bound = source.bind(request="Whatever")
    assert source.bindings == {}
    assert bound.bindings == {"request": "Whatever"}
    assert bound.users is source.users


def test_dict_source_actions():
    source = DictSource(
        users={
            "test": {
                "password": "test"
            },
        },
        title="test",
        description="Test of DictSource",
        actions=(Login,)
    )
    action = source.get(protocols.Challenge)
    assert isinstance(action, Login)

    action = source.get(protocols.Getter)
    assert action is None
