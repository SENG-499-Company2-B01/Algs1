import json

from models import Course

# Takes json as input, schedules the courses, and returns schedules for the input data
# Arguments:
# input_data: json object containing information of courses to be scheduled
# Returns: json representation of scheduled courses
def scheduler(input_data):
	#parsing input_data (json)
	data = json.loads(input_data)
	courses = []
	sessions = data["courses"][0]["Term"].keys() # getting list of sessions from input data
	for c in data["courses"]:
		for t,b in c["Term"].items():
			if b:
				course = Course(course_name = c["Course"], 
					course_size = c["Capacity"], 
					session = t, 
					prereqs = c["Prereqs"], 
					coreqs = c["Coreqs"])
				courses.append(course)

	# Scheduling Algorithm here

	# Scheduling Algorithm end

	return response(sessions, courses) # temporary, definitely should not work this way


# Parses data in a list of courses to the expected json output format
# Arguments:
# input_sessions: list of strings for sessions/terms
# courses: list of Course objects
# Returns: json representation of the course information
def response(input_sessions: list, courses: list):
	sessions = {s:[] for s in input_sessions}
	for c in courses:
		sessions[c.getSession()].append(c.getOutputDict())

	return json.dumps(sessions)


def main():
	pass

if __name__ == '__main__':
	main()