from src.apis.models import TimeBlock, Course

def naive_scheduler(courses, timeslots):
	index = 0
	for course in courses:
		course.changeInfo(times = timeslots[index])
		index += 1
		if index >= len(timeslots):
			index = 0
	return courses

def main():
	pass

if __name__ == '__main__':
	main()