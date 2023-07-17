from ..scheduler import cat_swarm

import random
import json
f=open("../../testing_subset.json","r")
data = f.read()
input_data=json.loads(data)
input_profs=input_data["users"]
input_courses=input_data["courses"]
input_classrooms=input_data["classrooms"]
f.close()
f=open("../../time_blocks.json","r")
data = f.read()
input_timeblocks = json.loads(data)
def test_cso():
    best_solution = cat_swarm.cat_swarm_optimization(input_profs, input_courses, input_classrooms, input_timeblocks, len(input_profs), 1000)
    assert best_solution['fitness'] >=0
    return 0
def fitness_room_assignments_test():
    class_id=random.randint(0, len(input_courses)-1)
    room_id=random.randint(0, len(input_classrooms)-1)
    assigned_class = input_courses[class_id]
    assigned_room = input_classrooms[room_id]
    # Check if the room capacity is sufficient
    if assigned_room['capacity'] < assigned_class['pre_enroll']:
        assert cat_swarm.fitness_room_assignments(input_classrooms,input_courses, class_id, room_id,0)==cat_swarm.ROOM_TOO_SMALL_PUNISHMENT
    else:
        assert cat_swarm.fitness_room_assignments(input_classrooms,input_courses, class_id, room_id,0)==0
    return 0
def preferred_course_match_test():
    # Increment fitness for each preferred course assigned
    professor_id=random.randint(0, len(input_profs)-1)
    assigned_class_id = random.randint(0, len(input_courses)-1)
    professor=input_profs[professor_id]
    assigned_class=input_courses[assigned_class_id]
    has_pref_flag = 0
    for course in professor['course_pref']:
        if "".join(course.split()) == assigned_class['course']:
            has_pref_flag = 1   
    if has_pref_flag == 1:
        assert cat_swarm.preferred_course_match(professor, assigned_class,0)==cat_swarm.PROFESSOR_PREFERRED_COURSE_MATCH_REWARD
    else:
        assert cat_swarm.preferred_course_match(professor, assigned_class,0)==cat_swarm.PROFESSOR_PREFERRED_COURSE_MATCH_PUNISHMENT
    return 0
def prof_maximum_courses_exceeded_constraint_test(professor, professor_assignments, professor_id, fitness):
    #get max course of each prof from input
    professor_id=random.randint(0, len(input_profs)-1)
    professor=input_profs[professor_id]
    professor_assignments=[random.randint(0,len(input_profs)-1) for n in range(len(input_classrooms))]
    max_course_val = professor["max_courses"]

    count_of_course_assignments = 0

    #get number of courses assigned to prof
    for profs in professor_assignments.items():
        if professor_id == profs:
            count_of_course_assignments += 1
    
    if count_of_course_assignments > max_course_val and max_course_val > 0:
        assert prof_maximum_courses_exceeded_constraint_test(professor,professor_assignments,professor_id,0)==cat_swarm.PROFESSOR_MAXIMUM_COURSES_EXCEEDED_PUNISHMENT
    else:
        assert prof_maximum_courses_exceeded_constraint_test(professor,professor_assignments,professor_id,0)==0
    return 0

def corequisite_coschedule_constraint(class_id, time_block, classes, class_timeslots, fitness):
    course_id=random.randint(0, len(input_courses)-1)
    randtime=random.choice(['A','B','C','D','E','F','G','H','I','L','M','N','O'])
    class_timeslots=[random.choice(['A','B','C','D','E','F','G','H','I','L','M','N','O']) for n in range(0,len(input_courses))]
    course = input_courses[course_id]
    input_timeblocks
    fitness=0
    #Find course corequisitesuate_fitness
    corequisite_list = course["corequisites"]
    if corequisite_list == None or len(corequisite_list) == 0:
        assert corequisite_coschedule_constraint(course_id,randtime,input_courses,class_timeslots,0)==0
    
    for coreqs_subarray in corequisite_list:
        #Iteratively go through each coreq and read corequisite_time_block   
        for coreq in coreqs_subarray:
            coreqs_course = list(filter(lambda x: x["shorthand"] == coreq, input_courses))[0]
            coreq_course_id = classes.index(coreqs_course)
            corequisite_time_block = class_timeslots[coreq_course_id]

            if corequisite_time_block == randtime:
                fitness += cat_swarm.COREQUISITE_COSCHEDULE_CONSTRAINT_PUNISHMENT
    
    assert  corequisite_coschedule_constraint(course_id,randtime,input_courses,class_timeslots,fitness)==fitness