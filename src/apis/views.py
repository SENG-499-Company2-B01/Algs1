#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

# SRS_CMP2 page 18
@api_view(['POST'])
def generate(request):
    # Do stuff to generate schedules here
    return Response({"message": "200 OK"})


# SRS_CMP2 page 19
@api_view(['POST'])
def verify(request):
    # Do stuff to verify schedules here
    return Response({"message": "200 OK"})
