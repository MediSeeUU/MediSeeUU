import datetime
from dataclasses import dataclass, field, asdict
import typing


@dataclass
class ParsedInfoStruct:
    eu_number: str = field(default_factory=str)
    parse_date: datetime.datetime = datetime.datetime.now()

    decisions: list[typing.Dict[str, str]] = field(default_factory=list)
    annexes: list[typing.Dict[str, str]] = field(default_factory=list)
    epars: list[typing.Dict[str, str]] = field(default_factory=list)
    omars: list[typing.Dict[str, str]] = field(default_factory=list)
