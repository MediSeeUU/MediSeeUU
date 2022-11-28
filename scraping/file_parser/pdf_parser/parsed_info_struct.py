import datetime
from dataclasses import dataclass, field, asdict
import typing
import scraping.definitions.attributes as attr

@dataclass
class ParsedInfoStruct:
    """
    Class continaining all information for a certain medicine:
    - EU number
    - Date of parsing the file
    - Attributes for each decision file
    - Attributes for each annex file
    - Attributes for each EPAR file
    - Attributes for each OMAR file
    """
    eu_number: str = field(default_factory=str)
    parse_date: datetime.datetime = datetime.datetime.now()

    attr.decision: list[typing.Dict[str, str]] = field(default_factory=list)
    attr.annex: list[typing.Dict[str, str]] = field(default_factory=list)
    attr.epar: list[typing.Dict[str, str]] = field(default_factory=list)
    attr.omar: list[typing.Dict[str, str]] = field(default_factory=list)
