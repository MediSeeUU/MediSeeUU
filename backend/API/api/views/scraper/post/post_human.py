# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from api.models.human_models import models
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
from .common import (
    pop_initial_histories_data,
    add_or_update_model,
    add_or_update_foreign_key,
    add_list,
    add_histories,
)


def post(data):
    if eu_pnumber := data.get("eu_pnumber"):
        override = data.get("override")
        # if variable is locked, delete it from the data
        locks = MedicineLocks.objects.filter(
            eu_pnumber=eu_pnumber
        ).values_list("column_name", flat=True)

        data = {key: value for key, value in data.items() if key not in locks}

        # pop initial histories from data to add them later because of circular dependency
        initial_history_data = pop_initial_histories_data(data, models)

        if active_substance := data.get("active_substance"):
            data["ingredients_and_substances"] = \
                add_or_update_model(data, override, IngredientsAndSubstances, {"active_substance": active_substance},
                                    IngredientsAndSubstancesSerializer, IngredientsAndSubstancesFlexVarUpdateSerializer)

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

        add_or_update_model(data, override, MedicinalProduct, {"eu_pnumber": eu_pnumber},
                            MedicinalProductSerializer, MedicinalProductFlexVarUpdateSerializer)

        add_or_update_model(data, override, MarketingAuthorisation, {"eu_pnumber": eu_pnumber},
                            MarketingAuthorisationSerializer, MarketingAuthorisationFlexVarUpdateSerializer)

        history_variables(eu_pnumber, initial_history_data, data)
        list_variables(eu_pnumber, data)

        add_or_update_model(initial_history_data, override, MedicinalProduct, {"eu_pnumber": eu_pnumber},
                            MedicinalProductSerializer, MedicinalProductFlexVarUpdateSerializer)

        add_or_update_model(initial_history_data, override, MarketingAuthorisation, {"eu_pnumber": eu_pnumber},
                            MarketingAuthorisationSerializer, MarketingAuthorisationFlexVarUpdateSerializer)


def list_variables(eu_pnumber, data):
    """
    Creates new list variables for the history models using the data given in its
    argument "data". It expects the input data for the list variable to be formed like this:
    ``name: ["value1", "value2", ...]``

    Args:
        data (medicineObject): The new medicine data.
    """
    add_list(
        "eu_pnumber",
        eu_pnumber,
        LegalBases,
        LegalBasesSerializer,
        "eu_legal_basis",
        data,
        True,
    )


def history_variables(eu_pnumber, initial_histories_data, current_histories_data):
    """
    Creates new history variables for the medicinal product history models using the data given in its
    argument "data". It expects the input data for the history variable to be formed like this:
    ``name: [{name: value, change_date: date}, ...]``

    Args:
        data (medicineObject): The new medicine data.
    """
    add_histories(
        "eu_pnumber",
        eu_pnumber,
        HistoryAuthorisationType,
        AuthorisationTypeSerializer,
        "eu_aut_type",
        "eu_aut_type_initial",
        initial_histories_data,
        "eu_aut_type_current",
        current_histories_data,
    )

    add_histories(
        "eu_pnumber",
        eu_pnumber,
        HistoryAuthorisationStatus,
        AuthorisationStatusSerializer,
        "eu_aut_status",
        "eu_aut_status_initial",
        initial_histories_data,
        "eu_aut_status_current",
        current_histories_data,
    )

    add_histories(
        "eu_pnumber",
        eu_pnumber,
        HistoryBrandName,
        BrandNameSerializer,
        "eu_brand_name",
        "eu_brand_name_initial",
        initial_histories_data,
        "eu_brand_name_current",
        current_histories_data,
    )

    add_histories(
        "eu_pnumber",
        eu_pnumber,
        HistoryOD,
        OrphanDesignationSerializer,
        "eu_od",
        "eu_od_initial",
        initial_histories_data,
        "eu_od_current",
        current_histories_data,
    )

    add_histories(
        "eu_pnumber",
        eu_pnumber,
        HistoryPrime,
        PrimeSerializer,
        "eu_prime",
        "eu_prime_initial",
        initial_histories_data,
        "eu_prime_current",
        current_histories_data,
    )

    add_histories(
        "eu_pnumber",
        eu_pnumber,
        HistoryMAH,
        MAHSerializer,
        "eu_mah",
        "eu_mah_initial",
        initial_histories_data,
        "eu_mah_current",
        current_histories_data,
    )

    add_histories(
        "eu_pnumber",
        eu_pnumber,
        HistoryEUOrphanCon,
        EUOrphanConSerializer,
        "eu_orphan_con",
        "eu_orphan_con_initial",
        initial_histories_data,
        "eu_orphan_con_current",
        current_histories_data,
    )

    return initial_histories_data

