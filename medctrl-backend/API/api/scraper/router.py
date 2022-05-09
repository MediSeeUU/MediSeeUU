from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.medicine_models import Medicine
from api.serializers.medicine_serializers import MedicineSerializer
from api.serializers.medicine_serializers import MedicineFlexSerializer
from api.models.medicine_models import Procedure
from api.serializers.medicine_serializers import ProcedureSerializer
from api.serializers.medicine_serializers import ProcedureFlexSerializer


class ScraperMedicine(APIView):
    """
    Class which provides an interface for the scraper to interact with the database.
    """

    def post(self, request, format=None):
        # get "medicine" key from request
        medicine = request.data.get("medicine")
        
        try:
            allobj = Medicine.objects.all()
            current = Medicine.objects.get(pk=medicine.get("eunumber"))
            
            
        # except:
        #     current = None
        
        finally:
            serializer = MedicineSerializer(current, data=medicine)
            serializer2 = MedicineFlexSerializer(current, data=medicine)
            if serializer2.is_valid():
                serializer2.save()
            print(serializer)
            print(serializer2)
            print(medicine)
            print(allobj)
            print(medicine.get("eunumber"))
            print(current)

            return Response("OK", status=200)

class ScraperProcedure(APIView):
    """
    Class which provides an interface for the scraper to interact with the database.
    """

    def post(self, request, format=None):
        # get "medicine" key from request
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
