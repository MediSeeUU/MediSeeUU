# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from typing import Any, Tuple
from django.contrib.auth.models import User
from django.db.models import Model
from rest_framework.serializers import Serializer
from api.views.other import permission_filter


def view_history(user: User, query_filter: dict[str, Any], models_serializers: list[Tuple[Model, Serializer]]) \
        -> list[dict[str, Any]]:
    """
    Creates a history timeline based on the models and serializers given, filtered by the user's permissions.

    Args:
        user (User): The user making the request to view the history.
        query_filter (dict[str, Any]): Filter for selecting the correct rows in the model.
        models_serializers (list[Tuple[Model, Serializer]]): The models and serializers used for the timeline.

    Returns:
        list[dict[str, Any]]: The history timeline.
    """
    histories = []
    for model, serializer in models_serializers:
        queryset = model.objects.filter(**query_filter).all()
        histories.append(serializer(queryset, many=True).data)

    perms = permission_filter(user)

    # Concat all histories
    histories = [inner for outer in histories for inner in outer]

    # Sort by change_date, ascending
    histories = sorted(histories, key=lambda d: d["change_date"])

    # filters histories according to access level of the user
    filtered_histories = [history for history in histories if all(key in perms for key in history.keys())]

    return filtered_histories
