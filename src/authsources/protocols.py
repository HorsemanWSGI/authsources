import typing as t
from authsources.identity import User, UserID


class RequestProtocol(t.Protocol):
    headers: dict


class Preflight(t.Protocol):

    def preflight(self, request: RequestProtocol):
        pass


class Getter(t.Protocol):

    def get(self, uid: UserID) -> User | None:
        pass


class Create(t.Protocol):

    def create(self, data: dict):
        pass


class Update(t.Protocol):

    def update(self, uid: UserID, data: dict) -> bool:
        pass


class Delete(t.Protocol):

    def delete(self, uid: UserID) -> bool:
        pass


class Search(t.Protocol):

    def search(
            self, criterions: dict, index: int = 0, size: int = 10
    ) -> t.Iterator[User]:
        pass

    def count(self, criterions: dict) -> int:
        pass


class Challenge(t.Protocol):

    def challenge(self, credentials: dict) -> User | None:
        pass


class ChangePassword(t.Protocol):

    def change_password(
            self, userid: UserID, new_value: str | bytes) -> bool:
        pass


class Groups(t.Protocol):

    def list_groups(self):
        pass

    def list_user_groups(self, userid: UserID):
        pass


class GroupCreate(t.Protocol):

    def create_group(self, data: dict, parent: str | None) -> bool:
        pass


class GroupDelete(t.Protocol):

    def delete_group(self, group_id: str) -> bool:
        pass


class GroupManage(t.Protocol):

    def list_group_users(self, groupid: str):
        pass

    def add_group_user(self, groupid: str, userid: str) -> bool:
        pass

    def remove_group_user(self, groupid: str, userid: str):
        pass
