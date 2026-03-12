import typing as t


class RequestProtocol(t.Protocol):
    headers: dict
