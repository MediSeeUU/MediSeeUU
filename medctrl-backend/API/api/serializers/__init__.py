"""
| The serializers package defines the packages used for serializing data.
| It is used to translate data from the database to python data and vice versa.
| It is divided into three packages:
|   The medicine_serializers is used for the human_models
|   The other package is used for the other models.
|   The user_serializers package is used for serializing user and group information.
| Read more about serializers here: https://docs.djangoproject.com/en/4.1/topics/serialization/
"""
# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from .other.saved_selection import SavedSelectionSerializer
