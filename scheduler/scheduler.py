import json

from Course import Course

'''
  "courses": {
    [{
      “Course”: “CSC 105”
      "Term": {
          "Winter”: false,
          “Spring”: true,
          “Summer”: true,
          }
      "Capacity": "40",
      "Prereqs": {
           "Abc 123",
       },
       "Coreqs": {
            "Def 456",
       }
    }]
  }
'''

def scheduler(input_data):
	data = json.loads(input_data)
	courses = []
	sessions = data["courses"].values()[0]["Term"].keys() # getting list of sessions from input data
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
	return response(sessions, courses)



def response(input_sessions, courses: list)
	sessions = {s:[] for s in input_sessions}
	for c in courses:
		sessions[c.getSession()].append(c.getOutputDict())

	return json.dumps(sessions)


def main():
	pass

if __name__ == '__main__':
	main()