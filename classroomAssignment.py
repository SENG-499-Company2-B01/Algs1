import json

def assign_courses(classrooms, time_blocks, schedule):
    # Sort classrooms by capacity in descending order
    for classroom in classrooms:
        if type(classroom['room']) == float:
            classroom['room'] = int(classroom['room'])
        classroom['classroom'] = classroom['shorthand'] + str(classroom['room'])
    sorted_classrooms = sorted(classrooms, key=lambda x: x['capacity'], reverse=True)

    # Initialize a dictionary to track classroom availability
    classroom_availability = {classroom['classroom']: {day: True for day in time_blocks.keys()} for classroom in classrooms}

    # Sort schedule by enrollment in descending order but add index for each course before to keep track of original order
    sorted_schedule = [{**d, 'index': i} for i, d in enumerate(schedule)]
    sorted_schedule = sorted(sorted_schedule, key=lambda x: max([sorted_schedule['enrollment'] for sorted_schedule in x['sections']]), reverse=True)
    
    assigned_courses = []
    
    for course in sorted_schedule:
        for section in course['sections']:
            enrolled_days = section['days']
            assigned_classroom = None

            # Get time block for section
            start_time = section['start_time'].replace(':', '')
            end_time = section['end_time'].replace(':', '')
            time_block = None

            for block, days in time_blocks.items():
                for day in days:
                    if enrolled_days == list(days.keys()) and days[day]['start'] == start_time and days[day]['end'] == end_time:
                        time_block = block
                        break

            # Iterate over sorted classrooms to find an available one
            for classroom in sorted_classrooms:
                classroom_name = classroom['classroom']
                classroom_days = classroom_availability[classroom_name]
                
                # Check if the classroom is available for the specific time block
                if classroom_days[time_block] == True:
                    # Assign the classroom and update its availability
                    assigned_classroom = classroom_name
                    classroom_days[time_block] = False
                
                if assigned_classroom:
                    break  # Break the loop if a classroom is assigned
                
            if assigned_classroom:
                assigned_courses.append({
                    'course': course['course'],
                    'section': course['sections'].index(section),
                    'classroom': assigned_classroom,
                    'index': course['index']
                })
                
    for course in assigned_courses:
        schedule[course['index']]['sections'][course['section'] - 1]['classroom'] = course['classroom']

    return {"courses": schedule}


def main():
    classrooms = json.load(open('testing_classrooms.json'))
    time_blocks = json.load(open('time_blocks.json'))
    schedule = json.load(open('mockSchedule.json'))

    schedule = assign_courses(classrooms, time_blocks, schedule['schedule'])

    json.dump(schedule, open('assigned_courses.json', 'w'), indent=4)

if __name__ == '__main__':
    main()
