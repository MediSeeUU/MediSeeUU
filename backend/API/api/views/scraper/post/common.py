# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from django.forms.models import model_to_dict
from api.models import models
from api.models.get_dashboard_columns import get_foreign_key_history_columns


def pop_foreign_key_histories_data(data):
    foreign_key_history_data = {}
    for foreign_key_history_column in get_foreign_key_history_columns(models):
        if foreign_key_history_column in data:
            foreign_key_history_data[foreign_key_history_column] = \
                data.pop(foreign_key_history_column)
    return foreign_key_history_data


def insert_data(data, current, serializer):
    """

    Args:
        data (medicineObject): The new medicine data.
        current (medicineObject): The medicine data that is currently in the database.
        serializer
    """
    medicine_serializer = serializer(current, data=data, partial=True)

    # update medicine
    if medicine_serializer.is_valid():
        inserted = medicine_serializer.save()
        return inserted.pk
    else:
        raise ValueError(medicine_serializer.errors)


def add_or_update_model(data, override, model, filters, insert_serializer, update_serializer):
    current_model_data = model.objects.filter(**filters).first()
    if override or not current_model_data:
        return insert_data(data, current_model_data, insert_serializer)
    else:
        update_null_values(data, current_model_data, insert_serializer)
        return insert_data(data, current_model_data, update_serializer)


def update_null_values(data, current, insert_serializer):
    """
    Updates all null values for an existing medicine using the data given in its
    argument "data".

    Args:
        data (medicineObject): The new medicine data.
        current_data (medicineObject): The medicine data that is currently in the database.
    """
    current_data = model_to_dict(current)
    new_data = {}

    for attr in current_data:
        if (getattr(current, attr) is None or getattr(current, attr) == "") and (
                not (data.get(attr) is None)
        ):
            new_data[attr] = data.get(attr)

    if len(new_data.keys()) >= 1:
        insert_data(new_data, current, insert_serializer)


def add_or_update_foreign_key(data, current, related_model, insert_serializer, update_serializer, attribute):
    if current:
        if hasattr(current, attribute):
            if foreign_key := getattr(current, attribute):
                current_related = related_model.objects.filter(
                    pk=foreign_key.pk
                ).first()
                if current_related:
                    data[attribute] = insert_data(data, current_related, update_serializer)
                    return None
    data[attribute] = insert_data(data, None, insert_serializer)


def add_list(pk_name, pk, model, serializer, name, data, replace):
    """
    Add a new object to the given list model.

    Args:
        model (medicine_model): The list model of the list object you want to add.
        serializer (medicine_serializer): The applicable serializer.
        name (string): The name of the attribute.
        data (medicineObject): The new medicine data.
        replace (bool): If True, will delete all previously added objects with the same eu_pnumber

    Raises:
        ValueError: Invalid data in data argument
        ValueError: Data does not exist in the given data argument
    """
    items = data.get(name)
    filters = {pk_name: pk}
    model_data = model.objects.filter(**filters).all()
    if items is not None and len(items) > 0:
        if model_data and replace:
            model_data.delete()
        if isinstance(items, list):
            for item in items:
                new_data = {name: item, pk_name: pk}
                insert_data(new_data, None, serializer)
        else:
            new_data = {name: items, pk_name: pk}
            insert_data(new_data, None, serializer)


def add_model_list(pk_name, pk, model, serializer, name, data, replace):
    """
    Add a new object to the given list model.

    Args:
        model (medicine_model): The list model of the list object you want to add.
        serializer (medicine_serializer): The applicable serializer.
        name (string): The name of the attribute.
        data (medicineObject): The new medicine data.
        replace (bool): If True, will delete all previously added objects with the same eu_pnumber

    Raises:
        ValueError: Invalid data in data argument
        ValueError: Data does not exist in the given data argument
    """
    items = data.get(name)
    filters = {pk_name: pk}
    model_data = model.objects.filter(**filters).all()
    if items is not None and len(items) > 0:
        if model_data and replace:
            model_data.delete()
        if isinstance(items, list):
            for item in items:
                new_data = item | {pk_name: pk}
                insert_data(new_data, None, serializer)
        else:
            new_data = items | {pk_name: pk}
            insert_data(new_data, None, serializer)


def add_histories(pk_name, pk, model, serializer, foreign_key_name,
                  foreign_key_data, current_name, current_data, name):
    """
    Add a new object to the given history model.

    Args:
        model (medicine_model): The history model of the history object you want to add.
        serializer (medicine_serializer): The applicable serializer.
        name (string): The name of the attribute.
        data (medicineObject): The new medicine data.

    Raises:
        ValueError: Invalid data in data argument
        ValueError: Data does not exist in the given data argument
    """
    foreign_key_item = foreign_key_data.get(foreign_key_name)
    foreign_key_data[foreign_key_name] = add_history(model, serializer, foreign_key_item, name, pk_name, pk)

    current_items = current_data.get(current_name)
    if current_items is not None and len(current_items) > 0:
        for item in current_items:
            add_history(model, serializer, item, name, pk_name, pk)


def add_history(model, serializer, data, name, pk_name, pk):
    """

    Args:
        model:
        serializer:
        data:
        name:
        pk_name:
        pk:

    Returns:

    """
    if data is not None:
        # Data to be inserted into the database
        data_value = data.get("value")
        if isinstance(data_value, dict):
            new_data = {"change_date": data.get("date"), pk_name: pk, **data_value}
        else:
            new_data = {"change_date": data.get("date"), name: data_value, pk_name: pk}
        # Select element in database with exact same data, so we don't insert an identical element
        current_data = model.objects.filter(**new_data).first()
        # return inserted element's primary key
        return insert_data(new_data, current_data, serializer)
