from authsources.errors import MagicLinkError, SourceError, UserExists


def test_user_exists():
    error = UserExists("email")
    assert isinstance(error, SourceError)
    assert error.field == "email"
    assert "email" in str(error)

    error = UserExists()
    assert error.field is None
    assert str(error) == "The user already exists."

    assert UserExists("email", "Taken.").message == "Taken."


def test_magic_link_error():
    error = MagicLinkError("no such user", 404)
    assert isinstance(error, SourceError)
    assert error.detail == "no such user"
    assert error.status == 404
    assert "404" in str(error)
