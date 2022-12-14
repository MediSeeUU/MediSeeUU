# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from api.models.get_dashboard_columns import get_initial_history_columns


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


def pop_initial_histories_data(data, models):
    initial_history_data = {}
    for initial_history_column in get_initial_history_columns(models):
        if initial_history_column in data:
            initial_history_data[initial_history_column] = \
                data.pop(initial_history_column)
    return initial_history_data
