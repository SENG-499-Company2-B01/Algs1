#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

# TODO: Temporary import
from .temp.dummy_schedule import get_dummy_schedule


# Create your views here.

# SRS_CMP2 page 18
@api_view(['POST'])
def generate(request):
    # TODO: Do stuff to generate schedules here
    courses = get_dummy_schedule()
    jsonData = request.data
    try:
        term = jsonData["term"]
        year = jsonData["year"]
        schedule = {
            "year": year, 
            "terms": [{
                "term": term,
                "courses": courses
            }]
        }
        return Response(schedule, status=200)
    except Exception as e:
        return Response(status=400)


# SRS_CMP2 page 19
@api_view(['POST'])
def verify(request):
    # Do stuff to verify schedules here
    return Response({"message": "200 OK"})
