#from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .scheduler.cat_swarm import main


# SRS_CMP2 page 18
@api_view(['POST'])
def generate(request):
    try:
        algs1_request = request.data
        users = algs1_request["users"]
        courses = algs1_request["courses"]
        classrooms = algs1_request["classrooms"]

        scheduled_courses = main(users, courses, classrooms)
        schedule = {
            "schedule": scheduled_courses
        }
        return Response(schedule, status=status.HTTP_200_OK)
    except Exception as e:
        response = {
            "error": str(e)
        }
        return JsonResponse(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['POST'])
def schedule(request):
    try:
        algs1_request = request.data
        professors = algs1_request["professors"]
        courses = algs1_request["courses"]
        classrooms = algs1_request["classrooms"]

        scheduled_courses = main(professors, courses, classrooms)
        schedule = {
            "schedule": scheduled_courses
        }
        return Response(schedule, status=status.HTTP_200_OK)
    except Exception as e:
        response = {
            "error": str(e)
        }
        return JsonResponse(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
