from authsources.sources.mapping import DictSource, DictUser


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
