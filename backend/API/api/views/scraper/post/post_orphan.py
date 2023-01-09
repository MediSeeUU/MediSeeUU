# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from api.models.orphan_models import (
    OrphanProduct,
    HistoryEUOrphanCon,
    HistoryEUODSponsor,
)
from api.serializers.medicine_serializers.scraper.post.orphan import (
    OrphanProductSerializer,
    EUOrphanConSerializer,
    EUODSponsorSerializer,
)
from api.serializers.medicine_serializers.scraper.update.orphan import (
    OrphanProductFlexVarUpdateSerializer,
)
from api.models.other import OrphanLocks
from .common import (
    pop_foreign_key_histories_data,
    add_or_update_model,
    add_or_update_foreign_key,
    add_list,
    add_histories,
)


def post(data):
    if eu_od_number := data.get("eu_od_number"):
        override = data.get("override")
        locks = OrphanLocks.objects.filter(
            eu_od_number=eu_od_number
        ).values_list("column_name", flat=True)

        data = {key: value for key, value in data.items() if key not in locks}

        foreign_key_history_data = pop_foreign_key_histories_data(data)

        add_or_update_model(data, override, OrphanProduct, {"eu_od_number": eu_od_number},
                            OrphanProductSerializer, OrphanProductFlexVarUpdateSerializer)


def list_variables(eu_od_number, data):
    """

    Args:
        eu_od_number:
        data:

    Returns:

    """


def history_variables(eu_od_number, foreign_key_histories_data, current_histories_data):
    """
    Creates new history variables for the orphan product history models using the data given in its
    argument "data". It expects the input data for the history variable to be formed like this:
    ``name: [{name: value, change_date: date}, ...]``

    Args:
        data (medicineObject): The new medicine data.
    """

    add_histories(
        "eu_od_number",
        eu_od_number,
        HistoryEUOrphanCon,
        EUOrphanConSerializer,
        "eu_orphan_con_initial",
        foreign_key_histories_data,
        "eu_orphan_con_current",
        current_histories_data,
        "indication",
    )

    add_histories(
        "eu_od_number",
        eu_od_number,
        HistoryEUODSponsor,
        EUODSponsorSerializer,
        "eu_od_sponsor",
        foreign_key_histories_data,
        "eu_od_sponsor",
        current_histories_data,
        "eu_od_sponsor",
    )
