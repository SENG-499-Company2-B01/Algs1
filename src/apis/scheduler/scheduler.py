import json
import sys

from src.apis.models import Course

# Takes json as input, schedules the courses, and returns schedules for the input data
# Arguments:
# input_data: json object containing information of courses to be scheduled
# Returns: json representation of scheduled courses
def scheduler(input_data):
	#parsing input_data (json)
	data = json.loads(input_data)
	courses = []
	sessions = data["courses"][0]["term"].keys() # getting list of sessions from input data

	# reading course information into course objects
	for c in data["courses"]:
		for t,b in c["term"].items():
			if b:
				course = Course(course_name = c["course"], 
					course_size = c["enrollment"], 
					session = t, 
					prereqs = c["prereqs"], 
					coreqs = c["coreqs"])
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
	if len(sys.argv) < 2:
		print("Usage: python scheduler.py path/to/input_data.json")
		exit()
	with open(sys.argv[1], 'r') as f:
		input_data = f.read()

	with open("test_output.json", 'w') as fo:
		fo.write(scheduler(input_data))

if __name__ == '__main__':
	main()