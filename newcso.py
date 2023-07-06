import random
import copy
import json
import math

VERY_LOW_VALUE = -50000

def evaluate_fitness(solution, professors, classes, rooms, time_blocks):
    # Extract information from the solution
    professor_assignments = solution['professor_assignments']
    room_assignments = solution['room_assignments']
    class_timeslots = solution['class_timeslots']
    
    # Initialize fitness score
    fitness = 0
    
    # Evaluate professor assignments
    for class_id, professor_id in professor_assignments.items():
        #print(professor_id)
        professor = professors[professor_id]
        assigned_class = classes[class_id]
        
        # Check if the professor is available
        if professor['unavailable'].get(class_timeslots[class_id]):
            fitness -= 1
        
        # # Check if the professor has preferences
        # if professor['course_pref'] and assigned_class['shorthand'] not in professor['course_pref']:
        #     fitness -= 1
        
        # Increment fitness for each preferred course assigned
        has_pref_flag = 0
        for course in professor['course_pref']:
            if course.replace(" ", "") == assigned_class['shorthand']:
                has_pref_flag = 1
                
        if has_pref_flag == 1:
            fitness += 5
            #print('nice')
        else:
            fitness -= 1
            #print('not nice')
                
        # Increment fitness for course below max limit
        res = 0
        for key in professor_assignments:
            if professor_assignments[key] == professor_id:
                res = res + 1
                
        if professor['max_courses'] > 0 and professor['max_courses'] >= res:
            fitness += 2

    # Evaluate room assignments
    for class_id, room_id in room_assignments.items():
        assigned_class = classes[class_id]
        assigned_room = rooms[room_id]
        assigned_class['capacity'] = 50 #change
        # Check if the room capacity is sufficient
        if assigned_room['capacity'] < assigned_class['capacity']:
            fitness -= 1
    
    
    #Evaluate time_block Assignments
    #todo
    #for class_id, time_block in class_timeslots.items():

    # Evaluate prof's clash fitness
    # list(set()) just returns the unique values in a list.
    assigned_profs = list(set(professor_assignments.values()))
    for prof in assigned_profs:
        courses_taught_by_prof = []

        # Assemble all courses taught by prof == prof_id
        for course_id, prof_id in professor_assignments.items():
            if prof_id == prof:
                courses_taught_by_prof.append(course_id)
        
        # Create list of timeblocks taught by prof == prof_id
        for course_id in courses_taught_by_prof:
            timeblock_for_courses_taught_by_prof = class_timeslots[course_id]
        
        # If the list of timeblocks taught by prof_id contains duplicates, 
        # it means the prof_id was assigned to teach more courses at same timeblock
        if(len(timeblock_for_courses_taught_by_prof) != len(list(set(timeblock_for_courses_taught_by_prof)))):
            fitness += VERY_LOW_VALUE
            break
        
        
    fitness += random.randint(-10,10)
    return fitness

def update_cat_position(cat, population, best_solution, c1, c2, w):
    for i in range(len(cat['position'])):
        r1 = random.random()
        r2 = random.random()
        #print(best_solution)
        #print(cat)
        cat['velocity'][i] = w * cat['velocity'][i] + c1 * r1 * (cat['best_position'][i] - cat['position'][i]) + c2 * r2 * (best_solution['best_position'][i] - cat['position'][i]) #best_solution['position'][i]
        # if cat['velocity'][i] < 1:
        #     cat['velocity'][i] = 1
        cat['position'][i] = round(cat['position'][i] + cat['velocity'][i])
        #print(cat['velocity'][i])
        # Apply boundary constraints if needed
        if cat['position'][i] < 0:
            cat['position'][i] = 0
        if cat['position'][i] >= len(population):
            cat['position'][i] = len(population) - 1
            

def cat_swarm_optimization(professors, classes, rooms, time_blocks, population_size, max_iterations):
    """
    # Initialize the population
    # population = []
    # for _ in range(population_size):
    #     solution = {
    #         'professor_assignments': {},
    #         'room_assignments': {},
    #         'class_timeslots': {}
    #     }
    #     for professor in professors:
    #         solution['professor_assignments'][professor['username']] = random.choice(list(range(len(classes))))
    #     for class_id, assigned_class in enumerate(classes):
    #         solution['room_assignments'][class_id] = random.choice(list(range(len(rooms))))
    #         solution['class_timeslots'][class_id] = random.choice(assigned_class['terms_offered'])
    #     population.append(solution)
    
    # # Main optimization loop
    # for iteration in range(max_iterations):
    #     # Evaluate fitness for each solution
    #     fitness_scores = []
    #     for solution in population:
    #         fitness_scores.append(evaluate_fitness(solution, professors, classes, rooms))
        
    #     # Select the best solution
    #     best_solution_index = fitness_scores.index(max(fitness_scores))
    #     best_solution = population[best_solution_index]
        
    #     # Update population using Cat Swarm Optimization algorithm
        
    #     # TODO: Add Cat Swarm Optimization logic here
        
    #     # Print the best fitness score for the current iteration
    #     print(f'Iteration {iteration + 1}: Best Fitness = {max(fitness_scores)}')
    
    # # Return the best solution found
    # return best_solution
    """
    population = []
    for _ in range(population_size):
        solution = {
            'professor_assignments': {},
            'room_assignments': {},
            'class_timeslots': {},
            'fitness': None
        }
        i=0
        # for professor in professors:
            
        #     solution['professor_assignments'][i] = random.choice(list(range(len(classes)))) # was classes
        #     i +=1
        for class_id, assigned_class in enumerate(classes):
            solution['professor_assignments'][class_id] = random.choice(list(range(len(professors)))) # was classes
            i +=1
            solution['room_assignments'][class_id] = random.choice(list(range(len(rooms))))
            solution['class_timeslots'][class_id] = random.choice(['A','B','C','D','E','F','G','H','I','L','M','N','O']) #was assigned_class['terms_offered']
        population.append(solution)
    
    # Initialize cat swarm
    swarm_size = 20  # Number of cats in the swarm
    c1 = 1.5  # Cognitive parameter
    c2 = 1.5 # Social parameter
    w = 0.5   # Inertia weight
    
    cats = []
    for _ in range(swarm_size):
        cat = {
            'position': [random.randint(0, population_size - 1) for _ in range(population_size)],
            'velocity': [random.uniform(-5, 5) for _ in range(population_size)],
            'best_position': None,
            'best_fitness': None
        }
        cats.append(cat)
    
    # Main optimization loop
    for iteration in range(max_iterations):
        # Evaluate fitness for each solution in population
        for solution in population:
            if solution['fitness'] is None:
                solution['fitness'] = evaluate_fitness(solution, professors, classes, rooms, time_blocks)
        
        # Update best solution found
        best_solution = max(population, key=lambda x: x['fitness'])
        # fitness_scores = []
        # for solution in population:
        #     fit = evaluate_fitness(solution, professors, classes, rooms, time_blocks)
        #     solution['fitness'] = fit
        #     fitness_scores.append(fit)
        
        # # Select the best solution
        # best_solution_index = fitness_scores.index(max(fitness_scores))
        # best_solution = population[best_solution_index]
        # Update best position and fitness for each cat
        for cat in cats:
            #print(population)
            #print(best_solution)
            #print(cat)
            cat_solution = copy.deepcopy(population[int(cat['position'][0])])
            for i in range(1, population_size):
                for class_id, professor_id in cat_solution['professor_assignments'].items():
                    cat_solution['professor_assignments'][class_id] = population[int(cat['position'][i])]['professor_assignments'][class_id]
                for class_id, room_id in cat_solution['room_assignments'].items():
                    cat_solution['room_assignments'][class_id] = population[int(cat['position'][i])]['room_assignments'][class_id]
                for class_id, time_id in cat_solution['class_timeslots'].items():
                    cat_solution['class_timeslots'][class_id] = population[int(cat['position'][i])]['class_timeslots'][class_id]
            
            cat_solution['fitness'] = evaluate_fitness(cat_solution, professors, classes, rooms, time_blocks)
            
            if cat['best_fitness'] is None or cat_solution['fitness'] > cat['best_fitness']:
                cat['best_position'] = cat['position']
                cat['best_fitness'] = cat_solution['fitness']
        
        # Update position and velocity for each cat
        best_cat = max(cats, key=lambda x: x['best_fitness'])
        for cat in cats:
            update_cat_position(cat, population, best_cat, c1, c2, w)
        
        # Update population with new solutions generated by cats
        for cat in cats:
            #print(cat)
            #print(population)
            new_solution = copy.deepcopy(population[int(cat['position'][0])])
            for i in range(1, population_size):
                for class_id, professor_id in new_solution['professor_assignments'].items():
                    new_solution['professor_assignments'][class_id] = population[int(cat['position'][i])]['professor_assignments'][class_id]
                for class_id, room_id in new_solution['room_assignments'].items():
                    new_solution['room_assignments'][class_id] = population[int(cat['position'][i])]['room_assignments'][class_id]
                for class_id, time_id in new_solution['class_timeslots'].items():
                    new_solution['class_timeslots'][class_id] = population[int(cat['position'][i])]['class_timeslots'][class_id]
            
            new_solution['fitness'] = evaluate_fitness(new_solution, professors, classes, rooms, time_blocks)
            
            if new_solution['fitness'] > population[int(cat['position'][0])]['fitness']:
                population[int(cat['position'][0])] = new_solution
    
        # Print the best fitness score for the current iteration
        print(f'Iteration {iteration + 1}: Best Fitness = {best_solution["fitness"]}')
    
    # Return the best solution found
    return best_solution


# Example usage
professors = [
    {
        "name": "Celina Berg",
        "username": "Celina.Berg",
        "peng": True,
        "pref_approved": False,
        "max_courses": 6,
        "course_pref": [
            "CSC111",
            "SENG310",
            "SENG435"
        ],
        "unavailable": {}
    }
]

classes = [
    {
        "name": "Fundamentals of Programming with Engineering Applications",
        "shorthand": "CSC111",
        "terms_offered": [
            "F",
            "Sp"
        ],
        "prerequisites": [
            []
        ],
        "corequisites": [],
        "capacity": 140
    }
]

rooms = [
    {
        "capacity": 140,
        "building": "BOB WRIGHT CENTRE",
        "room": "A104",
        "shorthand": "BWC"
    }
]

population_size = 50
max_iterations = 500

with open('testing_profs.json') as f:
    data = f.read()
    input_profs = json.loads(data)

with open('testing_courses.json') as f:
    data = f.read()
    input_courses = json.loads(data)

with open('testing_classrooms.json') as f:
    data = f.read()
    input_classrooms = json.loads(data)
    
with open('time_blocks.json') as f:
    data = f.read()
    input_timeblocks = json.loads(data)

best_solution = cat_swarm_optimization(input_profs, input_courses, input_classrooms, input_timeblocks, population_size, max_iterations)
timetable_list = []
print(best_solution)
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
        room = str(input_classrooms[room_num]['shorthand']) + " " + str(input_classrooms[room_num]['room'])
        num_seats = input_classrooms[room_num]['capacity']
        
        time_letter = best_solution['class_timeslots'][i]
        for key in input_timeblocks[time_letter].keys():
            days.append(key)
        start_time = input_timeblocks[time_letter][days[0]]["start"]
        end_time = input_timeblocks[time_letter][days[0]]["end"]
        
        section_dict['num'] = section
        section_dict['building'] = room
        section_dict['num_seats'] = num_seats
        section_dict['professor'] = prof
        section_dict['days'] = days
        section_dict['start_time'] = start_time
        section_dict['end_time'] = end_time
        
        sections_list.append(section_dict)
    
    timetable_dict['course'] = course['shorthand']
    timetable_dict['sections'] = sections_list
    timetable_list.append(timetable_dict)
    i += 1
    
json_timetable = json.dumps(timetable_list)

# Print the best solution
#print(best_solution)

print(json_timetable)