from django.urls import path
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.medicine_models import Medicine, Authorisation
from api.serializers.medicine_serializers import MedicineSerializer, AuthorisationSerializer, LookupStatusSerializer
from api.serializers.medicine_serializers import MedicineFlexVarUpdateSerializer
from api.models.medicine_models import Procedure
from api.serializers.medicine_serializers import ProcedureSerializer, AuthorisationFlexVarUpdateSerializer, ProcedureFlexSerializer
from api.models.medicine_models import Lookupstatus, Lookupactivesubstance, Lookupatccode, Lookuplegalbasis, Lookuplegalscope, Lookupmedicinetype, Lookuprapporteur
from api.serializers.medicine_serializers import LookupStatusSerializer, LookupActiveSubstanceSerializer, LookupAtccodeSerializer, LookupLegalbasisSerializer, LookupLegalscopeSerializer, LookupMedicinetypeSerializer, LookupRapporteurSerializer

class ScraperMedicine(APIView):
    """
    Class which provides an interface for the scraper to interact with the database.
    """

    def post(self, request, format=None):
        # get "medicine" key from request
        print(request.data)

        for medicine in request.data:
            print(medicine)
        
            currentMedicine = Medicine.objects.filter(pk=medicine.get("eunumber")).first()
            if currentMedicine:
                self.updateFlexMedicine(medicine, currentMedicine)
            else:
                self.addMedicine(medicine)

        return Response("OK", status=200)

    def updateFlexMedicine(self, data, current):
        currentAuthorisation = Authorisation.objects.filter(pk=data.get("eunumber")).first()
        print(currentAuthorisation)
        medicineSerializer = MedicineFlexVarUpdateSerializer(current, data=data)
        authorisationSerializer = AuthorisationFlexVarUpdateSerializer(currentAuthorisation, data=data)
        self.addLookup(Lookupstatus, LookupStatusSerializer(None, data=data), data.get("status"))
        self.addLookup(Lookupatccode, LookupAtccodeSerializer(None, data=data), data.get("atccode"))
        if (medicineSerializer.is_valid() and authorisationSerializer.is_valid()):
            medicineSerializer.save()
            authorisationSerializer.save()
    
    def addMedicine(self, data):
        serializer = MedicineSerializer(None, data=data)
        authorisationSerializer = AuthorisationSerializer(None, data=data)
        self.addLookup(Lookupstatus, LookupStatusSerializer(None, data=data), data.get("status"))
        self.addLookup(Lookupactivesubstance, LookupActiveSubstanceSerializer(None, data=data), data.get("activesubstance"))
        self.addLookup(Lookupatccode, LookupAtccodeSerializer(None, data=data), data.get("atccode"))
        self.addLookup(Lookuplegalbasis, LookupLegalbasisSerializer(None, data=data), data.get("legalbasis"))
        self.addLookup(Lookuplegalscope, LookupLegalscopeSerializer(None, data=data), data.get("legalscope"))
        self.addLookup(Lookupmedicinetype, LookupMedicinetypeSerializer(None, data=data), data.get("medicinetype"))
        self.addLookup(Lookuprapporteur, LookupRapporteurSerializer(None, data=data), data.get("rapporteur"))
        self.addLookup(Lookuprapporteur, LookupRapporteurSerializer(None, data={'rapporteur': data.get("corapporteur")}), data.get("corapporteur"))
        if serializer.is_valid():
            serializer.save()
        if authorisationSerializer.is_valid():
            authorisationSerializer.save()

    def addLookup(self, model, serializer, item):
        lookup = model.objects.filter(pk=item).first()
        print(serializer.is_valid())
        print(lookup)
        print(serializer)
        if not lookup and serializer.is_valid():
            print(item)
            print(serializer)
            serializer.save()

class ScraperProcedure(APIView):
    """
    Class which provides an interface for the scraper to interact with the database.
    """

    def post(self, request, format=None):
        # get "procedure" key from request
        procedure = request.data.get("procedure")
        
        try:
            allobj = Procedure.objects.all()
            current = Procedure.objects.get(pk=procedure.get("eunumber"))
            
            
        except:
            current = None
        
        finally:
            serializer = ProcedureSerializer(current, data=procedure)
            serializer2 = ProcedureFlexSerializer(current, data=procedure)
            # if serializer2.is_valid():
            #     serializer2.save()
            print(serializer)
            print(serializer2)
            print(procedure)
            print(allobj)
            print(procedure.get("eunumber"))
            print(current)

            return Response("OK", status=200)


url_patterns = [
    path("medicine", ScraperMedicine.as_view(), name="medicine"),
    path("procedure", ScraperProcedure.as_view(), name="procedure")
]
