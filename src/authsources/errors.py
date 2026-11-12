"""Source-neutral errors.

Raised by source actions instead of backend specific exceptions, so that
the code using a source does not need to know which backend answers.
"""


class SourceError(Exception):
    """Base class of the errors a source action may raise."""


class UserExists(SourceError):
    """The source refuses to create a user: it already exists.

    ``field`` names the conflicting property ("username" or "email"),
    if the source could tell.
    """

    def __init__(self, field: str | None = None, message: str | None = None):
        self.field = field
        self.message = message or (
            f"A user with the same {field} already exists." if field
            else "The user already exists.")
        super().__init__(self.message)


class MagicLinkError(SourceError):
    """The source could not issue a magic link.

    ``detail`` is a human readable reason, ``status`` the backend status
    code, if any.
    """

    def __init__(self, detail: str, status: int | None = None):
        self.detail = detail
        self.status = status
        super().__init__(f"Failed to create magic link ({status}): {detail}")
