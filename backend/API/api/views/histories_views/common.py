# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from typing import Any, Tuple
from django.contrib.auth.models import User
from django.db.models import Model
from rest_framework.serializers import Serializer
from api.views.other import permission_filter


def view_history(user: User, models_serializers: list[Tuple[Model, Serializer, dict[str, str]]]) \
        -> list[dict[str, Any]]:
    """
    Creates a history timeline based on the models and serializers given, filtered by the user's permissions.

    Args:
        user (User): The user making the request to view the history.
        models_serializers (list[Tuple[Model, Serializer]]): The models and serializers used for the timeline.

    Returns:
        list[dict[str, Any]]: The history timeline.
    """
    histories = []
    for model, serializer, query_filter in models_serializers:
        queryset = model.objects.filter(**query_filter).all()
        histories.append(serializer(queryset, many=True).data)

    # for eu_orphan_con, concat histories
    new_histories = []
    for history in histories:
        new_history = []
        for item in history:
            if data := item.pop("history", None):
                for new_item in data:
                    new_history.append(new_item)
            else:
                new_history.append(item)
        new_histories.append(new_history)

    # Concat all histories
    histories = [item for history in new_histories for item in history]

    # Sort by change_date, ascending
    histories = sorted(histories, key=lambda d: d["change_date"])

    perms = permission_filter(user)

    # filters histories according to access level of the user
    filtered_histories = [history for history in histories if all(key in perms for key in history.keys())]

    return filtered_histories
