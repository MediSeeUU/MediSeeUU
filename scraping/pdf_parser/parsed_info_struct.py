import datetime
import typing
from dataclasses import dataclass, field, asdict


@dataclass
class ParsedInfoStruct:
    """
    Class containing all information for a certain medicine:
    - EU number
    - Date of parsing the file
    - Attributes for each decision file
    - Attributes for each annex file
    - Attributes for each EPAR file
    - Attributes for each OMAR file
    - Filename of each ODWAR file
    """
    eu_number: str = field(default_factory=str)
    parse_date: datetime.datetime = datetime.datetime.now().strftime("%Y-%m-%d")

    decisions: list[typing.Dict[str, str]] = field(default_factory=list)
    annexes: list[typing.Dict[str, str]] = field(default_factory=list)
    epars: list[typing.Dict[str, str]] = field(default_factory=list)
    omars: list[typing.Dict[str, str]] = field(default_factory=list)
    odwars: list[typing.Dict[str, str]] = field(default_factory=list)
