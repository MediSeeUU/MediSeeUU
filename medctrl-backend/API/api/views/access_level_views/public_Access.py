from api.models.medicine_models.medicine import Medicine
from rest_framework.response import Response

def publicAccess(request):
    columns = Medicine.objects.all()
    print("OUTPUT...........................................................................................", columns)
    print(columns[0].eunumber)
    return Response() 