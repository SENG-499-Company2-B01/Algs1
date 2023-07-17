#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import random

from .scheduler.cat_swarm import main


# SRS_CMP2 page 18
@api_view(['POST'])
def generate(request):
    try:
        algs1_request = request.data
        term = algs1_request["term"]
        year = algs1_request["year"]
        users = algs1_request["users"]
        courses = algs1_request["courses"]
        classrooms = algs1_request["classrooms"]

        # def in_term(course):
        #     match term.lower():
        #         case "fall":
        #             return "fall" in [x.strip().lower() for x in course["terms_offered"]]
        #         case "summer":
        #             return "summer" in [x.strip().lower() for x in course["terms_offered"]]
        #         case "spring":
        #             return "spring" in [x.strip().lower() for x in course["terms_offered"]]
                
        # term_courses = list(filter(in_term, courses))
        # for course in courses:
        #     if "pre_enroll" not in course:
        #         course["pre_enroll"] = random.randint(80, 100)
        scheduled_courses = main(users, courses, classrooms)
        schedule = {
            "year": year, 
            "terms": [{
                "term": term,
                "courses": scheduled_courses
            }]
        }    
        return Response(schedule, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)