# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from enum import Enum, auto


class Headers(Enum):
    GeneralInformation = "General Information"

def createField(field, header : Headers, data_format):
    setattr(field, "header", header.value)
    setattr(field, "data_format", data_format)
    return field