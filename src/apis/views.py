#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# TODO: Temporary import
from .temp.dummy_schedule import get_dummy_schedule


# Create your views here.

# SRS_CMP2 page 18
@api_view(['POST'])
def generate(request):
    # TODO: Do stuff to generate schedules here
    schedule = get_dummy_schedule()
    return Response(schedule)


# SRS_CMP2 page 19
@api_view(['POST'])
def verify(request):
    # Do stuff to verify schedules here
    return Response({"message": "200 OK"})
