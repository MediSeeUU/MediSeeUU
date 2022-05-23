from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.medicine_serializers import (
    AuthorisationFlexVarUpdateSerializer,
    MedicineFlexVarUpdateSerializer,
    MedicineSerializer,
    AuthorisationSerializer,
    LookupStatusSerializer,
    LookupActiveSubstanceSerializer,
    LookupAtccodeSerializer,
    LookupLegalbasisSerializer,
    LookupLegalscopeSerializer,
    LookupMedicinetypeSerializer,
    LookupRapporteurSerializer,
)
from api.models.medicine_models import (
    Lookupstatus,
    Lookupactivesubstance,
    Lookupatccode,
    Lookuplegalbasis,
    Lookuplegalscope,
    Lookupmedicinetype,
    Lookuprapporteur,
    Medicine,
    Authorisation,
)


class ScraperMedicine(APIView):
    """
    Class which provides an interface for the scraper to interact
    with the database models medicine and authorisation.
    """

    # Permission on this endpoint when user can add medicine
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        """
        Specify queryset for DjangoModelPermissions
        """
        return Medicine.objects.all()

    def post(self, request):
        """
        Post endpoint medicine scraper
        """
        # initialize list to return failed updates/adds, so these can be checked manually
        failed_medicines = []
        # get "medicine" key from request
        for medicine in request.data:
            try:
                # check if medicine already exists based on eunumber
                current_medicine = Medicine.objects.filter(
                    pk=medicine.get("eunumber")
                ).first()
                # if exists update the medicine otherwise add it,
                # update works only on flexible variables
                if current_medicine:
                    status = self.update_flex_medicine(medicine, current_medicine)
                else:
                    status = self.add_medicine(medicine)
                # if status is failed, add medicine to the failed list
                if not status:
                    failed_medicines.append(medicine)
            except:
                failed_medicines.append(medicine)

        return Response(failed_medicines, status=200)

    def update_flex_medicine(self, data, current):
        """
        Update flexible medicine variables
        """
        current_authorisation = Authorisation.objects.filter(
            pk=data.get("eunumber")
        ).first()
        medicine_serializer = MedicineFlexVarUpdateSerializer(current, data=data)
        authorisation_serializer = AuthorisationFlexVarUpdateSerializer(
            current_authorisation, data=data
        )
        # add variables to lookup table
        add_lookup(
            Lookupstatus, LookupStatusSerializer(None, data=data), data.get("status")
        )
        add_lookup(
            Lookupatccode, LookupAtccodeSerializer(None, data=data), data.get("atccode")
        )
        # if authorisation not exists, add authorisation
        if not current_authorisation:
            authorisation_serializer = authorisation_serializer(None, data=data)

        # update medicine and authorisation
        if medicine_serializer.is_valid() and authorisation_serializer.is_valid():
            medicine_serializer.save()
            authorisation_serializer.save()
            return True
        return False

    def add_medicine(self, data):
        """
        add medicine variables
        """
        # initialise serializers voor addition
        serializer = MedicineSerializer(None, data=data)
        authorisation_serializer = AuthorisationSerializer(None, data=data)
        # add variables to lookup table
        add_lookup(
            Lookupstatus, LookupStatusSerializer(None, data=data), data.get("status")
        )
        add_lookup(
            Lookupactivesubstance,
            LookupActiveSubstanceSerializer(None, data=data),
            data.get("activesubstance"),
        )
        add_lookup(
            Lookupatccode, LookupAtccodeSerializer(None, data=data), data.get("atccode")
        )
        add_lookup(
            Lookuplegalbasis,
            LookupLegalbasisSerializer(None, data=data),
            data.get("legalbasis"),
        )
        add_lookup(
            Lookuplegalscope,
            LookupLegalscopeSerializer(None, data=data),
            data.get("legalscope"),
        )
        add_lookup(
            Lookupmedicinetype,
            LookupMedicinetypeSerializer(None, data=data),
            data.get("medicinetype"),
        )
        add_lookup(
            Lookuprapporteur,
            LookupRapporteurSerializer(None, data=data),
            data.get("rapporteur"),
        )
        add_lookup(
            Lookuprapporteur,
            LookupRapporteurSerializer(
                None, data={"rapporteur": data.get("corapporteur")}
            ),
            data.get("corapporteur"),
        )
        # add medicine and authorisation
        if serializer.is_valid():
            serializer.save()
        else:
            return False
        if authorisation_serializer.is_valid():
            authorisation_serializer.save()
        else:
            return False
        return True


# if item does not exist in the database (model), add it with the serializer
def add_lookup(model, serializer, item):
    lookup = model.objects.filter(pk=item).first()
    if not lookup and serializer.is_valid():
        serializer.save()
