from rest_framework import views
from django.http import JsonResponse
from rest_framework.response import Response
from django.core import serializers
from rest_framework import generics, permissions
from .medicine_info_json import get_medicine_info

class Medicine_info(views.APIView):
    """
    Viewset for the Medicine info
    """

    def get(self, request):
        return Response(get_medicine_info())