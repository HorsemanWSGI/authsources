import typing as t
import abc
import uuid
from authsources.abc.identity import User
from authsources.abc.source import Source
from authsources.abc.protocols import RequestProtocol


class Authenticator(abc.ABC):

    sources: dict[str, Source]

    @abc.abstractmethod
    def challenge(
            self, request: RequestProtocol, credentials: t.Any
    ) -> User | None:
        pass

    @abc.abstractmethod
    def identify(
            self, request: RequestProtocol
    ) -> User: ...

    @abc.abstractmethod
    def forget(
            self, request: RequestProtocol
    ) -> None: ...

    @abc.abstractmethod
    def remember(
            self, request: RequestProtocol, source_id: str, user: User
    ) -> None: ...
