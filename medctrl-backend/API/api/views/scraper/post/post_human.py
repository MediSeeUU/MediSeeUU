from django.forms.models import model_to_dict
from api.models.human_models import (
    MedicinalProduct,
    IngredientsAndSubstances,
    MarketingAuthorisation,
    AcceleratedAssessment,
    Duration,
    Procedures,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon,
    LegalBases,
)
from api.models.other import MedicineLocks
from api.serializers.medicine_serializers.scraper.post.human import (
    MedicinalProductSerializer,
    IngredientsAndSubstancesSerializer,
    MarketingAuthorisationSerializer,
    AcceleratedAssessmentSerializer,
    DurationSerializer,
    ProceduresSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
    EUOrphanConSerializer,
    LegalBasesSerializer,
)
from api.serializers.medicine_serializers.scraper.update.human import (
    MedicinalProductFlexVarUpdateSerializer,
    IngredientsAndSubstancesFlexVarUpdateSerializer,
    MarketingAuthorisationFlexVarUpdateSerializer,
    AcceleratedAssessmentFlexVarUpdateSerializer,
    DurationFlexVarUpdateSerializer,
)
from api.models.other import MedicineLocks
from .common import insert_data


def post(data):
    if eu_pnumber := data.get("eu_pnumber"):
        override = data.get("override")
        # if variable is locked, delete it from the data
        locks = MedicineLocks.objects.filter(
            eu_pnumber=eu_pnumber
        ).values_list("column_name", flat=True)

        data = {key: value for key, value in data.items() if key not in locks}

        current_ingredients_and_substances = None
        if active_substance := data.get("active_substance"):
            current_ingredients_and_substances = IngredientsAndSubstances.objects.filter(
                active_substance=active_substance
            ).first()
        data["ingredients_and_substances"] = \
            insert_data(data, current_ingredients_and_substances, IngredientsAndSubstancesFlexVarUpdateSerializer) \
            if current_ingredients_and_substances else \
            insert_data(data, current_ingredients_and_substances, IngredientsAndSubstancesSerializer)

        current_marketing_authorisation = MarketingAuthorisation.objects.filter(
            eu_pnumber=eu_pnumber
        ).first()

        add_or_update_foreign_key(
            data,
            current_marketing_authorisation,
            AcceleratedAssessment,
            AcceleratedAssessmentSerializer,
            AcceleratedAssessmentFlexVarUpdateSerializer,
            "ema_accelerated_assessment"
        )
        add_or_update_foreign_key(
            data,
            current_marketing_authorisation,
            Duration,
            DurationSerializer,
            DurationFlexVarUpdateSerializer,
            "duration"
        )

        current_medicinal_product = MedicinalProduct.objects.filter(
            eu_pnumber=eu_pnumber
        ).first()

        insert_data(data, current_medicinal_product, MedicinalProductSerializer)

        insert_data(data, current_marketing_authorisation, MarketingAuthorisationSerializer)

        history_variables(data)
        list_variables(data)


def add_or_update_model(data, model, ):
    pass


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


def add_or_override_medicine(data, eu_pnumber):
    """
    Adds a new medicine with its attributes to the database. If this is valid,
    it will also add the history variables to the database.

    Args:
        data (medicineObject): The new medicine data.
        eu_pnumber (str): The EU number of the human medicine being added

    Raises:
        ValueError: Invalid data in data argument
    """
    # initialise serializers for addition
    current_medicine = MedicinalProduct.objects.filter(
        eu_pnumber=eu_pnumber
    ).first()
    serializer = MedicinalProductSerializer(current_medicine, data=data, partial=True)

    # add medicine and authorisation
    if serializer.is_valid():
        serializer.save()
    else:
        raise ValueError(serializer.errors)


def update_null_values(data, current_medicine):
    """
    Updates all null values for an existing medicine using the data given in its
    argument "data".

    Args:
        data (medicineObject): The new medicine data.
        current_medicine (medicineObject): The medicine data that is currently in the database.
    """
    medicine = model_to_dict(current_medicine)
    new_data = {"eu_pnumber": data.get("eu_pnumber")}

    for attr in medicine:
        if (getattr(current_medicine, attr) is None or getattr(current_medicine, attr) == '') and (
                not (data.get(attr) is None)
        ):
            new_data[attr] = data.get(attr)

    if len(new_data.keys()) > 1:
        add_or_override_medicine(new_data, current_medicine)


def list_variables(data):
    """
    Creates new list variables for the history models using the data given in its
    argument "data". It expects the input data for the list variable to be formed like this:
    ``name: ["value1", "value2", ...]``

    Args:
        data (medicineObject): The new medicine data.
    """
    add_list(
        LegalBases,
        LegalBasesSerializer,
        "eu_legal_basis",
        data,
        True,
    )


def add_list(model, serializer, name, data, replace):
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
    eu_pnumber = data.get("eu_pnumber")
    items = data.get(name)
    model_data = model.objects.filter(eu_pnumber=eu_pnumber).all()

    if items is not None and len(items) > 0:
        for item in items:
            if model_data and replace:
                model_data.delete()
            serializer = serializer(
                None, {name: item, "eu_pnumber": eu_pnumber}
            )
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(f"{name} contains invalid data! {serializer.errors}")


def history_variables(data):
    """
    Creates new history variables for the medicinal product history models using the data given in its
    argument "data". It expects the input data for the history variable to be formed like this:
    ``name: [{name: value, change_date: date}, ...]``

    Args:
        data (medicineObject): The new medicine data.
    """
    add_histories(
        HistoryAuthorisationType,
        AuthorisationTypeSerializer,
        data,
        "eu_aut_type",
        "eu_aut_type_initial",
        "eu_aut_type_current",
    )

    add_histories(
        HistoryAuthorisationStatus,
        AuthorisationStatusSerializer,
        data,
        "eu_aut_status",
        "eu_aut_status_initial",
        "eu_aut_status_current",
    )

    add_histories(
        HistoryBrandName,
        BrandNameSerializer,
        data,
        "eu_brand_name",
        "eu_brand_name_initial",
        "eu_brand_name_current",
    )

    add_histories(
        HistoryOD,
        OrphanDesignationSerializer,
        data,
        "eu_od",
        "eu_od_initial",
        "eu_od_current",
    )

    add_histories(
        HistoryPrime,
        PrimeSerializer,
        data,
        "eu_prime",
        "eu_prime_initial",
        "eu_prime_current",
    )

    add_histories(
        HistoryMAH,
        MAHSerializer,
        data,
        "eu_mah",
        "eu_mah_initial",
        "eu_mah_current",
    )

    add_histories(
        HistoryEUOrphanCon,
        EUOrphanConSerializer,
        data,
        "eu_orphan_con",
        "eu_orphan_con_initial",
        "eu_orphan_con_current",
    )


def add_histories(model, serializer, data, name, initial_name=None, current_name=None):
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
    eu_pnumber = data.get("eu_pnumber")

    if current_name:
        current_items = data.get(current_name)
        if current_items is not None and len(current_items) > 0:
            for item in current_items:
                add_history(model, serializer, item, name, eu_pnumber)

    if initial_name:
        initial_item = data.get(initial_name)
        return add_history(model, serializer, initial_item, name, eu_pnumber)


def add_history(model, serializer, data, name, eu_pnumber):
    if data is not None:
        new_data = {"change_date": data.get("date"), name: data.get("value"), "eu_pnumber": eu_pnumber}
        current_data = model.objects.filter(**new_data).first()
        return insert_data(new_data, current_data, serializer)
