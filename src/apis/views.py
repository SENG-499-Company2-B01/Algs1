#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import random

from .scheduler.cat_swarm import main


# SRS_CMP2 page 18
@api_view(['POST'])
def generate(request):
    algs1_request = request.data
    try:
        term = algs1_request["term"]
        year = algs1_request["year"]
        users = algs1_request["users"]
        courses = algs1_request["courses"]
        classrooms = algs1_request["classrooms"]
        capacity = algs1_request["capacity"]

        def in_term(course):
            match term.lower():
                case "fall":
                    return "fall" in [x.strip().lower() for x in course["terms_offered"]]
                case "summer":
                    return "summer" in [x.strip().lower() for x in course["terms_offered"]]
                case "spring":
                    return "spring" in [x.strip().lower() for x in course["terms_offered"]]
                
        term_courses = list(filter(in_term, courses))
        
        for course in term_courses:
            if "estimates" in capacity:
                for courseEstimate in capacity["estimates"]:
                    if courseEstimate["course"] == course["shorthand"]:
                        course["num_seats"] = courseEstimate["estimate"]
            if "num_seats" not in course:
                course["num_seats"] = random.randint(80, 100)
        scheduled_courses = main(users, term_courses, classrooms)
        schedule = {
            "year": year, 
            "terms": [{
                "term": term,
                "courses": scheduled_courses
            }]
        }    
        return Response(schedule, status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# SRS_CMP2 page 19
@api_view(['POST'])
def verify(request):
    # Do stuff to verify schedules here
    return Response({"message": "200 OK"}, status=status.HTTP_200_OK)
