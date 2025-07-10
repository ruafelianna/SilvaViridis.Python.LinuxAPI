from collections.abc import Generator

from .core import Context

class Attributes:
    def get(self, attribute : str | bytes, default : bytes | None = None) -> bytes | None: ...

class Device:
    @property
    def device_type(self) -> str | None: ...

    @property
    def sys_path(self) -> str: ...

    @property
    def sys_name(self) -> str: ...

    @property
    def parent(self) -> Device | None: ...

    @property
    def children(self) -> Generator[Device]: ...

    @property
    def attributes(self) -> Attributes: ...

    def find_parent(self, subsystem : str, device_type : str | None = None) -> Device | None: ...

class Enumerator:
    def __iter__(self) -> Generator[Device]: ...

class Devices:
    @classmethod
    def from_path(cls, context : Context, path : str) -> Device: ...
