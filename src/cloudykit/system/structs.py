import typing
import dataclasses as dt
from pathlib import Path


__all__ = (
    "ManagerConfig",
    "PathConfig",
    "Error"
)


@dt.dataclass(frozen=True, eq=False)
class ManagerConfig:
    import_string: typing.Optional[str]
    mount: bool = dt.field(default=False)
    args: tuple = dt.field(default_factory=tuple)
    kwargs: dict = dt.field(default_factory=dict)


@dt.dataclass(frozen=True, eq=False)
class PathConfig:
    root: Path
    section: str = dt.field(default=None)
    section_stem: bool = dt.field(default=False)
    pattern: str = dt.field(default="*.json")


@dt.dataclass
class Error:
    title: str
    code: str = dt.field(default="error")
    description: str = dt.field(default="Some error has been occurred")
    exception: Exception = dt.field(default_factory=Exception)
    raise_error: bool = dt.field(default=False)
