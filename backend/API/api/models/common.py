# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from enum import Enum

generic_na_values = [
    "Not found",
    "Not available at time of document publication",
    "Value should be present in source",
]


class DataFormats(Enum):
    String = ("string", generic_na_values)
    Number = ("number", generic_na_values)
    Bool = ("bool", generic_na_values)
    Date = ("date", generic_na_values + ["Date is left blank in source"])
    Link = ("link", generic_na_values)
    String_List = ("[string]", generic_na_values)
    Dictionary_List = ("[dict]", generic_na_values)

    @property
    def data_format(self):
        return self.value[0]

    @property
    def na_values(self):
        return self.value[1]


class NAChoices(models.enums.ChoicesMeta):
    @property
    def choices(self):
        return super().choices + [(value, value) for value in DataFormats.String.na_values]


class AutTypes(models.TextChoices, metaclass=NAChoices):
    """
    Choice types for eu_aut_type. Is derived from the enumerated choice class.
    """
    CONDITIONAL = "conditional",
    EXCEPTIONAL = "exceptional",
    STANDARD = "standard"
    UNCERTAIN = "exceptional or conditional"


class AutStatus(models.TextChoices, metaclass=NAChoices):
    """
    Choice types for eu_aut_status. Is derived from the enumerated choice class.
    """
    ACTIVE = "ACTIVE",
    WITHDRAWAL = "WITHDRAWN",
    REFUSALS = "REFUSED"


class LegalBasesTypes(models.TextChoices, metaclass=NAChoices):
    """
    Choice types for legal bases. Is derived from the enumerated choice class.
    """
    article4_8 = "article 4.8",
    article4_8_1 = "article 4.8.1",
    article4_8_2 = "article 4.8.2",
    article4_8_3 = "article 4.8.3",
    article8_3 = "article 8.3"
    article_10_1 = "article 10.1"
    article_10_2 = "article 10.2"
    article_10_3 = "article 10.3"
    article_10_4 = "article 10.4"
    article_10_a = "article 10.a"
    article_10_b = "article 10.b"
    article_10_c = "article 10.c"
