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
