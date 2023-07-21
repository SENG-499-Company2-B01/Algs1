import random
import copy
import json
from datetime import datetime, timedelta
import numpy as np
import heapq
import math
import time
#Punishments
VERY_LOW_VALUE = -50000
ROOM_TOO_SMALL_PUNISHMENT = -10000
PROFESSOR_PREFERRED_COURSE_MATCH_PUNISHMENT = -1
PROFESSOR_MAXIMUM_COURSES_EXCEEDED_PUNISHMENT = -10000
COREQUISITE_COSCHEDULE_CONSTRAINT_PUNISHMENT = -10000 # Gets cumulated for every coreq mismatch pairs. 
PROFESSOR_UNAVAILABLE_TIMEBLOCK = -5000
PROF_NOT_PENG_CLASS_REQ_PENG = -500

#Rewards
PROFESSOR_PREFERRED_COURSE_MATCH_REWARD = 5
PREREQ_SAME_TIME_REWARD = 10
PROFESSOR_PREFERRED_TIMEBLOCK = 5
PROF_PENG_CLASS_REQ_PENG = 20

def fitness_room_assignments(classes, rooms, class_id, room_id, fitness):
    assigned_class = classes[class_id]
    #print(room_id)
    assigned_room = rooms[room_id]
    # Check if the room capacity is sufficient
    # print(assigned_room['capacity'])
    # print(assigned_class['pre_enroll'])
    if assigned_room['capacity'] < assigned_class['pre_enroll']:
        fitness += ROOM_TOO_SMALL_PUNISHMENT
        #print(1)
    else:
        fitness += 1
    return fitness
                    
# Moving Dylan's preferred courses fitness function to a separate function
def preferred_course_match(professor, assigned_class, fitness):
    # Increment fitness for each preferred course assigned
    has_pref_flag = 0
    for course in professor['course_pref']:
        #if course.replace(" ", "") == assigned_class['course']:
        if course == assigned_class['course']:
            has_pref_flag = 1
                
    if has_pref_flag == 1:
        fitness += PROFESSOR_PREFERRED_COURSE_MATCH_REWARD
        #print('nice')
    else:
        fitness += PROFESSOR_PREFERRED_COURSE_MATCH_PUNISHMENT
        #print('not nice')
        #print(2)
    return fitness

def prof_maximum_courses_exceeded_constraint(professor, professor_assignments, professor_id, fitness):
    #get max course of each prof from input
    max_course_val = professor["max_courses"]

    count_of_course_assignments = 0

    #get number of courses assigned to prof
    for profs in professor_assignments.items():
        if professor_id == profs:
            count_of_course_assignments += 1
    
    if count_of_course_assignments > max_course_val and max_course_val > 0:
        fitness += PROFESSOR_MAXIMUM_COURSES_EXCEEDED_PUNISHMENT
        #print(3)
    return fitness

def corequisite_coschedule_constraint(class_id, time_block, classes, class_timeslots, fitness):
    course = classes[class_id]

    #Find course corequisites
    corequisite_list = course["corequisites"]
    if corequisite_list == None or len(corequisite_list) == 0:
        return fitness
    
    for coreqs_subarray in corequisite_list:
        #Iteratively go through each coreq and read corequisite_time_block   
        for coreq in coreqs_subarray:
            coreqs_course = list(filter(lambda x: x["shorthand"] == coreq, classes))[0]
            coreq_course_id = classes.index(coreqs_course)
            corequisite_time_block = class_timeslots[coreq_course_id]

            if corequisite_time_block == time_block:
                fitness += COREQUISITE_COSCHEDULE_CONSTRAINT_PUNISHMENT
    return fitness

def prof_timepref_constraint(professor, class_timeslots, class_id, time_blocks,fitness):
    #print(professor['timeblocks'].get(class_timeslots[class_id]))
    #is assigned to a prefered timeblock
    time_blocks_letter = chr(ord('@')+int(time_blocks))
    if professor['timeblocks'].get(time_blocks_letter):
        fitness += PROFESSOR_PREFERRED_TIMEBLOCK
        
    else:
        fitness += PROFESSOR_UNAVAILABLE_TIMEBLOCK
        #print(5)
    return fitness

def fitness_prerequisites(classes,class_timeslots, class_id, fitness):
    assigned_class = classes[class_id]
    for group in assigned_class["prerequisites"]:
        for pq in group:
            prereq = next((i for i, item in enumerate(classes) if item["course"].replace(" ","") == pq.replace(" ","")), None)
            if prereq != None:
                if class_timeslots[prereq] == class_timeslots[class_id]:
                    fitness += PREREQ_SAME_TIME_REWARD
    return fitness

#fitness function if a course requires a peng and check to see if professor has peng
def prof_peng_constraint(professor, assigned_class, fitness):
    
    if assigned_class["peng"] == True and professor["peng"] == False:
        fitness += PROF_NOT_PENG_CLASS_REQ_PENG
        #print(6)
    elif assigned_class["peng"] == True and professor["peng"] == True:
        fitness += PROF_PENG_CLASS_REQ_PENG
    return fitness

def evaluate_fitness(solution, professors, classes, rooms, time_blocks):
    # Extract information from the solution
    professor_assignments = solution['professor_assignments']
    room_assignments = solution['room_assignments']
    class_timeslots = solution['class_timeslots']
    # print(solution)
    # print(professors)
    # print(professors[0])
    #print(rooms)
    # time.sleep(5)
    # Initialize fitness score
    fitness = 0
    
    # Evaluate professor assignments
    for class_id, professor_id in professor_assignments.items():
        #print(professor_id)

        professor = professors[professor_id]
        assigned_class = classes[class_id]
        
        for class_id, time_block in class_timeslots.items():
            #print(class_timeslots[class_id])
            time_block_num = class_timeslots[class_id]
            #print(time_block_letter)
            fitness = prof_timepref_constraint(professor, class_timeslots, class_id, time_block_num, fitness)
        fitness = prof_peng_constraint(professor, assigned_class, fitness)
        # # Check if the professor has preferences
        # if professor['course_pref'] and assigned_class['course'] not in professor['course_pref']:
        #     fitness -= 1

        fitness = preferred_course_match(professor, assigned_class, fitness)

        fitness = prof_maximum_courses_exceeded_constraint(professor, professor_assignments ,professor_id, fitness)
                
        # Increment fitness for course below max limit
        res = 0
        for key in professor_assignments:
            if professor_assignments[key] == professor_id:
                res = res + 1
                
        if professor['max_courses'] > 0 and professor['max_courses'] >= res:
            fitness += 2

    # Evaluate room assignments
    for class_id, room_id in room_assignments.items():
        #print(room_id)
    
        #print(rooms[room_id])
        #time.sleep(5)
        fitness = fitness_room_assignments(classes, rooms, class_id, room_id, fitness)    
    
    #Evaluate time_block Assignments
    for class_id, time_block in class_timeslots.items():
        time_block_num = class_timeslots[class_id]
        time_block_letter = chr(ord('@')+int(time_block_num))
        fitness = corequisite_coschedule_constraint(class_id, time_block_letter, classes, class_timeslots, fitness)
        fitness = fitness_prerequisites(classes,class_timeslots,class_id,fitness)

    # Evaluate prof's clash fitness
    # list(set()) just returns the unique values in a list.
    assigned_profs = list(set(professor_assignments.values()))
    for prof in assigned_profs:
        courses_taught_by_prof = []
        timeblock_for_courses_taught_by_prof = []
        
        # Assemble all courses taught by prof == prof_id
        for course_id, prof_id in professor_assignments.items():
            if prof_id == prof:
                courses_taught_by_prof.append(course_id)

        # Create list of timeblocks taught by prof == prof_id
        for course_id in courses_taught_by_prof:
            timeblock_for_courses_taught_by_prof = chr(ord('@')+class_timeslots[course_id])

        # If the list of timeblocks taught by prof_id contains duplicates, 
        # it means the prof_id was assigned to teach more courses at same timeblock
        if(len(timeblock_for_courses_taught_by_prof) != len(list(set(timeblock_for_courses_taught_by_prof)))):
            fitness += VERY_LOW_VALUE
            print(7)
            break
        
    #fitness += random.randint(-10,10)
    return fitness

def update_cat_position(cat, population, best_solution, c1, c2, w, max_prof_range, max_room_range, max_timeblock_range):
    ranges = [max_prof_range, max_room_range, max_timeblock_range]
    for i in range(len(cat['position'])):
        r1 = random.random() 
        r2 = random.random()
        # print(best_solution)
        # print(cat['position'])
        #print(cat['velocity'][i])
        #cat['velocity'][i] = w * cat['velocity'][i] + c1 * r1 * (cat['best_position'][i] - cat['position'][i]) + c2 * r2 * (best_solution['best_position'][i] - cat['position'][i]) #best_solution['position'][i]
        for j in range(len(cat['position'][i])):
            #print(cat['velocity'][i][j])
            cat['velocity'][i][j] = w * cat['velocity'][i][j] + c1 * r1 * (best_solution['best_position'][i][j] - cat['position'][i][j]) #best_solution['position'][i]

            
            # if cat['velocity'][i] < 1 and cat['velocity'][i] > 0:
            #     cat['velocity'][i] = 1
            # elif cat['velocity'][i] > -1 and cat['velocity'][i] < 0:
            #     cat['velocity'][i] = -1
            range_val = (0.2*ranges[i])
            #cat['velocity'][i][j] = [max(min(number, range_val), -range_val) for number in list(cat['velocity'][i])]
            cat['velocity'][i] = np.clip(cat['velocity'][i], -range_val, range_val).tolist()
            cat['position'][i][j] = round(cat['position'][i][j] + cat['velocity'][i][j])
            #print(cat['velocity'][i])
            #Apply boundary constraints if needed
            if cat['position'][i][j] < 0:
                cat['position'][i][j] = 0
            if cat['position'][i][j] >= ranges[i]:
                cat['position'][i][j] = ranges[i] - 1
    return cat
            

def cat_swarm_optimization(professors, classes, rooms, time_blocks, population_size, max_iterations):
    # Initialize the population
    population = []
    best_solution = {}
    best_solution_total = {}
    cats = []
    best_cats = []
    best_solutions = {}    
    max_class_range = len(classes) 
    max_prof_range = len(professors) -1 
    max_room_range = len(rooms) -1
    max_timeblock_range = len(time_blocks)-1
    ranges = [max_prof_range, max_room_range, max_timeblock_range]
    dim = 3 #dimention of solution
    swarm_size = population_size  # Number of cats in the swarm
    c1 = 1  # Cognitive parameter
    c2 = 1.5 # Social parameter
    w = 0.5   # Inertia weight
    spc = True #self-position considering
    smp = 3 #seeking memory pool
    cdc = 1 #counts of dimension to change 80% maybe
    srd = 0.2 #seeking range of the selected dimension
    mr = 10 #number of cats that hunt 
    top_n = 2 #number of cats to hold as best
    #vmax = 0.2*range
    
    ww = w
    cc1 = c1
    
    # Initialize cat swarm
    num_tracing = int(((mr * swarm_size) / 100))
    for _ in range(population_size):
        solution = {
            'professor_assignments': {},
            'room_assignments': {},
            'class_timeslots': {},
            'fitness': None
        }

        cat = {}
        # for professor in professors:
            
        #     solution['professor_assignments'][i] = random.choice(list(range(len(classes)))) # was classes
        #     i +=1
        for class_id, assigned_class in enumerate(classes):
            solution['professor_assignments'][class_id] = random.choice(list(range(len(professors)))) # was classes
            solution['room_assignments'][class_id] = random.choice(list(range(len(rooms))))
            solution['class_timeslots'][class_id] = random.choice(list(range(len(time_blocks)))) #['A','B','C','D','E','F','G','H','I','L','M','N','O']
            
        cat = {
            'position': [list(solution['professor_assignments'].values()),list(solution['room_assignments'].values()),list(solution['class_timeslots'].values())],
            #'velocity': [list(np.random.uniform(-(0.2*max_prof_range),0.2*max_prof_range,max_class_range))[0],list(np.random.uniform(-(0.2*max_room_range),0.2*max_room_range,max_class_range))[0],list(np.random.uniform(-(0.2*max_timeblock_range),0.2*max_timeblock_range,max_class_range))[0]],
            'velocity': [[random.uniform(-(0.2*max_prof_range),0.2*max_prof_range) for _ in range(max_class_range)],[random.uniform(-(0.2*max_room_range),0.2*max_room_range) for _ in range(max_class_range)],[random.uniform(-(0.2*max_timeblock_range),0.2*max_timeblock_range) for _ in range(max_class_range)]],
            'best_position': None,
            'best_fitness': None,
            'cat_seek': True
            }
        cat['best_position'] = cat['position']
        population.append(solution)
        cats.append(cat)
        #print(cat['position'])
    i=0    
    for solution in population:    
        if solution['fitness'] is None:
            solution['fitness'] = evaluate_fitness(solution, professors, classes, rooms, time_blocks)
            cats[i]['best_fitness'] = solution['fitness']
        i += 1
        
    
    
    # for _ in range(swarm_size):
    #     cat = {
    #         'position': [random.randint(0, population_size - 1) for _ in range(population_size)],
    #         'velocity': [random.uniform(-5, 5) for _ in range(population_size)],
    #         'best_position': None,
    #         'best_fitness': None
    #     }
    #     cat['best_position'] = cat['position']
    #     cats.append(cat)
        # print(cat['velocity'])
        # print(cat['position'])
    #Evaluate fitness for each solution in population
    # for solution in population:    
    #     if solution['fitness'] is None:
    #         solution['fitness'] = evaluate_fitness(solution, professors, classes, rooms, time_blocks)
            
    # best_solution = max(population, key=lambda x: x['fitness'])
    # Main optimization loop
    for iteration in range(max_iterations):
        
        best_solutions['best'] = max(population, key=lambda x: x['fitness'])
        best_solutions['best2'] = heapq.nlargest(2, population, key=lambda x: x['fitness'])[1]
        best_cats.append(max(cats, key=lambda x: x['best_fitness']))
        best_cats.append(heapq.nlargest(2, cats, key=lambda x: x['best_fitness'])[1])

        for cat in cats:
            cat['cat_seek'] = True
        for _ in range(num_tracing):
            cats[random.randint(0, swarm_size-1)]['cat_seek'] = False
        
    
        # Evaluate fitness for each solution in population
        # for solution in population:
        #     if solution['fitness'] is None:
        #         solution['fitness'] = evaluate_fitness(solution, professors, classes, rooms, time_blocks)
        #print(population)
        # Update best solution found
        # best_solution = max(population, key=lambda x: x['fitness'])
        # fitness_scores = []
        # for solution in population:
        #     fit = evaluate_fitness(solution, professors, classes, rooms, time_blocks)
        #     solution['fitness'] = fit
        #     fitness_scores.append(fit)
        
        # # Select the best solution
        # best_solution_index = fitness_scores.index(max(fitness_scores))
        # best_solution = population[best_solution_index]
        # Update best position and fitness for each cat
        i=0
        best_solution_seek = {'fitness':None}
        best_solution_trace = {'fitness':None}
        
        for cat in cats:
            #print(population)
            #print(best_solution)
            #print(cat)
            
            #cat seek
            cat_copies = []
            if cat['cat_seek'] == True:
                
                for _ in range(smp):
                    cat_copies.append(copy.deepcopy(cat)) 
                #print(cat_copies)
                cat_solutions =[]
                for cat_num in range(len(cat_copies)-1):
                    for _ in range(cdc):
                        tmp = random.randint(0, dim-1)
                        
                        for posi in range(len(cat_copies[cat_num]['position'][tmp])):
                        
                            cat_copies[cat_num]['position'][tmp][posi] = int(cat_copies[cat_num]['position'][tmp][posi] + (cat_copies[cat_num]['position'][tmp][posi] * random.choice([-1,1]) * srd))
                            cat_copies[cat_num]['position'][tmp] = np.clip(cat_copies[cat_num]['position'][tmp], 0, ranges[tmp]).tolist()
                            # print(cat_copies[cat_num]['position'][tmp])
                
                
                    cat_solution = copy.deepcopy(population[i])
                    #for pos in range(max_class_range):
                    for class_id, professor_id in cat_solution['professor_assignments'].items():
                        cat_solution['professor_assignments'][class_id] = cat_copies[cat_num]['position'][0][class_id]
                    for class_id, room_id in cat_solution['room_assignments'].items():
                        cat_solution['room_assignments'][class_id] = cat_copies[cat_num]['position'][1][class_id]
                    for class_id, time_id in cat_solution['class_timeslots'].items():
                        cat_solution['class_timeslots'][class_id] = cat_copies[cat_num]['position'][2][class_id]

                    #print(cat_solution)
                    #time.sleep(2)
                    cat_solution['fitness'] = evaluate_fitness(cat_solution, professors, classes, rooms, time_blocks)
                    cat_solutions.append(cat_solution)
                
                cat_solutions.append(population[i])
                best_solution = max(cat_solutions, key=lambda x: x['fitness'])
                
                best_num = 0
                for cat_num in range(1,len(cat_copies)):
                    if cat_solutions[cat_num]['fitness'] > cat_solutions[best_num]['fitness']:
                        best_num = cat_num
                        
                if cat['best_fitness'] is None or best_solution['fitness'] > cat['best_fitness']:
                    cat['best_position'] = cat_copies[best_num]['position']
                    cat['best_fitness'] = best_solution['fitness']
                    population[i] = best_solution
                    cats[i] = cat
                
                if best_solution_seek['fitness'] is None or best_solution_seek['fitness'] < best_solution['fitness']:
                    best_solution_seek = best_solution
                    
        
        
                    # for pos in range(max_class_range):
                    # for class_id, professor_id in population[i]['professor_assignments'].items():
                    #     cat_solution['professor_assignments'][class_id] = population[cat['position'][0]]['professor_assignments'][class_id]
                    # for class_id, room_id in population[i]['room_assignments'].items():
                    #     cat_solution['room_assignments'][class_id] = population[cat['position'][i]]['room_assignments'][class_id]
                    # for class_id, time_id in population[i]['class_timeslots'].items():
                    #     cat_solution['class_timeslots'][class_id] = population[cat['position'][i]]['class_timeslots'][class_id]
            
                    # cat_solution['fitness'] = evaluate_fitness(cat_solution[i], professors, classes, rooms, time_blocks)
                    # cat_solutions.append()
                    
                    # if cat['best_fitness'] is None or cat_solution[i]['fitness'] > cat['best_fitness']:
                    #     cat['best_position'] = cat['position']
                    #     cat['best_fitness'] = cat_solution['fitness']
    
            # for i in range(1, population_size):
            #     cat_solution = copy.deepcopy(population[int(cat['position'][i])])
            #     #cat_solution.append(population[int(cat['position'][i])])
            #     cat_solution['fitness'] = evaluate_fitness(cat_solution, professors, classes, rooms, time_blocks)

            #     if cat['best_fitness'] is None or cat_solution['fitness'] > cat['best_fitness']:
            #         cat['best_position'] = cat['position']
            #         cat['best_fitness'] = cat_solution['fitness']
            
            #cat trace
            else:
                cat_solution2 = {}
                # Update position and velocity for each cat
                # print(best_cats[0])
                # time.sleep(5)
                cat = update_cat_position(cat, population, best_cats[0], cc1, cc1, ww, max_prof_range, max_room_range, max_timeblock_range)
                
                
                cat_solution2 = copy.deepcopy(population[i])
                #for pos in range(max_class_range):
                for class_id, professor_id in cat_solution2['professor_assignments'].items():
                    cat_solution2['professor_assignments'][class_id] = cat['position'][0][class_id]
                for class_id, room_id in cat_solution2['room_assignments'].items():
                    cat_solution2['room_assignments'][class_id] = cat['position'][1][class_id]
                for class_id, time_id in cat_solution2['class_timeslots'].items():
                    cat_solution2['class_timeslots'][class_id] = cat['position'][2][class_id]
            
                cat_solution2['fitness'] = evaluate_fitness(cat_solution2, professors, classes, rooms, time_blocks)
                
            
                if cat['best_fitness'] is None or cat_solution2['fitness'] > cat['best_fitness']:
                    cat['best_position'] = cat['position']
                    cat['best_fitness'] = cat_solution2['fitness']
                    population[i] = cat_solution2
                    cats[i] = cat
                    
                if best_solution_trace['fitness'] is None or best_solution_trace['fitness'] < cat['best_fitness']:
                    best_solution_trace = population[i]
                
                
                # # Update population with new solutions generated by cats
                # for cat in cats:
                #     #print(cat)
                #     #print(population)
                #     new_solution = copy.deepcopy(population[int(cat['position'][0])])
                #     for i in range(1, population_size):
                #         for class_id, professor_id in new_solution['professor_assignments'].items():
                #             new_solution['professor_assignments'][class_id] = population[int(cat['position'][i])]['professor_assignments'][class_id]
                #         for class_id, room_id in new_solution['room_assignments'].items():
                #             new_solution['room_assignments'][class_id] = population[int(cat['position'][i])]['room_assignments'][class_id]
                #         for class_id, time_id in new_solution['class_timeslots'].items():
                #             new_solution['class_timeslots'][class_id] = population[int(cat['position'][i])]['class_timeslots'][class_id]
                    
                #     new_solution['fitness'] = evaluate_fitness(new_solution, professors, classes, rooms, time_blocks)
                    
                #     # if new_solution['fitness'] > population[int(cat['position'][0])]['fitness']:
                #     #     population[int(cat['position'][0])] = new_solution
                #     if new_solution['fitness'] > population[int(cat['position'][0])]['fitness']:
                #         population[int(cat['position'][0])] = new_solution
            
            cats[i]['position'] = cat['position']
            i += 1
            
        #ww = w + (max_iterations - iteration) / (2 * max_iterations)
        #cc1 = c1 - (max_iterations - iteration) / (2 * max_iterations)
        
        # best_cats.append(max(cats, key=lambda x: x['fitness']))
        # best_cats.append(heapq.nlargest(2, cats, key=lambda x: x['fitness'])[1])
        
        best_solution_total = max(population, key=lambda x: x['fitness'])            
        # Print the best fitness score for the current iteration
        print(f'Iteration {iteration + 1}: Best Fitness = {best_solution_total["fitness"]}')
    
    # Return the best solution found
    return best_solution_total

def time_in_range(start, end, x):
    #Return true if x is in the range [start, end]
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def main(input_profs, input_courses, input_classrooms):

    population_size = 25
    #max_iterations = 500
    max_iterations = 20

    with open('/app/time_blocks.json') as f:
        data = f.read()
        input_timeblocks = json.loads(data)
    #convert input_profs time_pref to time_block
    
    for prof in input_profs:
        timeblock_pref_dict = {}
        for time_list_outer in prof['time_pref'].keys():
            for time_list_count in range(len(prof['time_pref'][time_list_outer])):
                
                    
                start_time = datetime.strptime(prof['time_pref'][time_list_outer][time_list_count][0], '%H:%M')
                end_time = datetime.strptime(prof['time_pref'][time_list_outer][time_list_count][1], '%H:%M')
                
                for time_letter in input_timeblocks.keys():
                    add_time_flag = 0
                    for day in input_timeblocks[time_letter].keys():
                        class_start = datetime.strptime(input_timeblocks[time_letter][day]["start"], '%H:%M')
                        class_end = datetime.strptime(input_timeblocks[time_letter][day]["end"], '%H:%M')
                        if time_in_range(start_time,end_time,class_start) and time_in_range(start_time,end_time,class_end):
                            add_time_flag = 1
                        else:
                            add_time_flag = 0
                            break
                    if add_time_flag == 1:
                        timeblock_pref_dict[time_letter] = input_timeblocks[time_letter]
        #print(timeblock_pref_dict)
        prof['timeblocks'] = timeblock_pref_dict

            
            
    best_solution = cat_swarm_optimization(input_profs, input_courses, input_classrooms, input_timeblocks, population_size, max_iterations)
    timetable_list = []

    i = 0
    for course in input_courses:
        timetable_dict = {}
        sections = ["A01"] #I dont account for splitting yet
        sections_list = []
        for section in sections:
            days = []
            section_dict = {}
            #prof_num = list(best_solution['professor_assignments'].keys())[list(best_solution['professor_assignments'].values()).index(i)]
            prof_num = best_solution['professor_assignments'][i]
            prof = input_profs[prof_num]["name"]
            
            room_num = best_solution['room_assignments'][i]
            building = input_classrooms[room_num]["building"]
            room = input_classrooms[room_num]["room"]
            pre_enroll = course['pre_enroll']
            room_seats = input_classrooms[room_num]["capacity"]
            
            time_letter = best_solution['class_timeslots'][i]
            time_letter = chr(ord("@")+int(time_letter))
            for key in input_timeblocks[time_letter].keys():
                days.append(key)
            start_time = input_timeblocks[time_letter][days[0]]["start"]
            end_time = input_timeblocks[time_letter][days[0]]["end"]
            
            section_dict['num'] = section
            section_dict['building'] = building
            section_dict['room'] = room
            section_dict['num_seats'] = pre_enroll
            section_dict['num_enroll'] = room_seats
            section_dict['professor'] = prof
            section_dict['days'] = days
            section_dict['start_time'] = start_time
            section_dict['end_time'] = end_time
            
            sections_list.append(section_dict)
        
        timetable_dict['course'] = course['course']
        timetable_dict['sections'] = sections_list
        timetable_list.append(timetable_dict)
        i += 1
    
    return timetable_list
