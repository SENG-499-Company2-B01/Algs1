
import random
import datetime

#declarations of file names
fp = None
fp1 = None
fp2 = None
fp3 = None
fp4 = None

# definitions of variables and constants
class_name_length = 15 # maximum length of a class's name
class_name = ['' for x in range (teacher_name_length)] 
teacher_name_length = 50 # maximum length of a teacher's name
teacher_name = ['' for x in range (teacher_name_length)]
classes_no1 = 50 # maximum number of classes
teachers_no1 = 100 # maximum number of teachers

# basic parameters of the fitness function
BASE = 1.3
HCW = 10

# parameters of the CSO algorithm
SMP = 2 # seeking memory pool - number of positions to consider during cat_seek procedure
SRD = 10 # seeking range of the selected dimension - percentage of change of each dimension
CDC = 10 # count of dimensions to change - percentage of dimensions to change
SPC = 1 # self position consideration - if it equals to 1 the cat will also consider its current position during cat_seek procedure
MR = 4 # mixture ratio - percentage of cats in tracing mode
cats = 30 # number of cats
iterations = 5000 # number of iterations of core process

def SwapInt(x,y,tmp):
	tmp = x
	x = y
	y = tmp

numSlots = 35
x = [[[0 for i in range(numSlots)] for j in range(classes_no1)] for k in range(cats)] # matrix for storing a cat's data
global_best = [[0 for i in range(numSlots)] for j in range (classes_no1)] # matrix for storing the global best cat
v = [[0 for i in range(numSlots)] for j in range[classes_no1]] # helper array

inf = 10e13 # worst (maximum) value of the fitness function

global_best_fitness = inf # best (minimum) value of the fitness function
fitness = inf # current value of the fitness function

# variables for counting the time that passed
begin_time = None
last_updating_time = 0.0

there_is_coteaching = 0 # this is 1 if there is co-teaching, else it is 0
co_class = [[0 for i in range(teachers_no1)] for j in range(classes_no1)] # contains the class with which there is co-teaching
co_teacher = [[0 for i in range(classes_no1)] for j in range(teachers_no1)] # contains the teacher that participates in a co-teaching

# definition of the teacher's record
class teacher_record:
	def __init__(self,
			surname: str = '',
			kind: int = 0,
			total_hours: int = 0,
			remaining_hours: int = 0,
			availability_hours: int = 0,
			availability_days: int = 0,
			is_available_at_day: list = [1,1,1,1,1],
			unavailable_timeslots: list = [1 for i in range(numSlots)],
			classes_he_teaches: list = [[0 for i in range(3)] for j in range(classes_no1)],
			num_of_classes: int = 0,
			coteachings: list = [[0 for i in range(5)] for j in range(15)],
			count_of_coteachers: int = 0):
		self.surname = surname
		self.kind = kind
		self.total_hours = total_hours
		self.remaining_hours = remaining_hours
		self.availability_hours = availability_hours
		self.availability_days = availability_days
		self.is_available_at_day = is_available_at_day
		self.unavailable_timeslots = unavailable_timeslots
		self.classes_he_teaches = classes_he_teaches
		self.num_of_classes = num_of_classes
		self.coteachings = coteachings
		self.count_of_coteachers = count_of_coteachers

teachers = [teacher_record() for i in range(teachers_no1)]

class class_record:
	def __init__(self,
			class_number: int = 0,
			class_name: str,
			hours_per_week: int = 0,
			remaining_hours: int = 0,
			teachers_of_class_and_hours: list = [[0 for i in range(3)] for j in range(numSlots)],
			number_of_teachers: int = 0,
			teachers_of_class_and_hours_remaining: list = [[0 for i in range(3)] for j in range(numSlots)]):
		self.class_number = class_number
		self.class_name = class_name
		self.hours_per_week = hours_per_week
		self.remaining_hours = remaining_hours
		self.teachers_of_class_and_hours = teachers_of_class_and_hours
		self.number_of_teachers = number_of_teachers
		self.teachers_of_class_and_hours_remaining = teachers_of_class_and_hours_remaining

classes = [class_record() for i in range(classes_no1)]

def initiliaze_randomness(seed: int = -1): # initializes the seed, if seed is -1 then it uses system time as seed
	if seed == -1:
		seed = datetime.datetime.now().timestamp()
	random.seed(seed)
	return seed

def randint(lower: int, upper: int): # returns a random integer between lower and upper
	return lower + random.randint() % (upper-lower+1)

def randd(x0: float, x1: float): # returns a random double/float between x0 and x1
	return random.uniform(x0,x1)

def unique_randint(a: list, lower: int, upper: int, number: int): # returns an array with all the integers between lower and upper in random order
	for x in range(number):
		a[x] = lower + random.randint() % (upper - lower + 1)
		if x == 0:
			continue
		
		for y in range(x):
			if a[x] == a[y]:
				y = 0
				a[x] = lower + random.randint() % (upper - lower + 1)

				while a[x] == a[y]:
					a[x] = lower + random.randint() % (upper - lower + 1)
			else:
				continue

	id_ = 0
	for x in range(number):
		id_ += a[x]

	return id_

def round_num(number:float): # returns the rounded double number
	return int(number+0.5) if (number >= 0) else int(number-0.5)


# -------------------- FUNCTIONS RELATED TO THE FITNESS VALUE --------------------
def check_wrong_coteaching(to_file,
		begin: int,
		end: int,
		a: list,
		number_of_classes1: int,
		show_results = 0): # checks if there are wrong co-teachings and returns the relevant cost
	number_of_cases = 0

	for start in range(begin, end,7):
		for t in range(start,start+7):
			for i in range(number_of_classes1):
				for j in range(classes[i].number_of_teachers):
					first_teacher = classes[i].teachers_of_class_and_hours[j][0]
					second_class = co_class[i][first_teacher]
					if second_class != -1:
						co_teacher1 = co_teacher[first_teacher][second_class]
					else:
						co_teacher1 = 2015

					if second_class != -1 and second_class != i:
						if co_teacher1 != 2015 and a[i][t] == first_teacher and a[second_class][t] != co_teacher1:
							number_of_cases += 1

	cost = number_of_cases * HCW * pow(2*BASE,BASE)

	if show_results == 1:
		print(f"Total number of wrong co-teaching is {number_of_cases}")
	if to_file == 33:
		fp3.write(f"Total number of wrong co-teaching is {number_of_cases}")
		fp3.write(f"Cost wrong co-teaching is {cost}")
	return cost

def swap(a:list, class1: int, timeslow1: int, timeslot2: int):
	temp = a[class1][timeslot1]
	a[class1][timeslot1] = a[class1][timeslot2]
	a[class1][timeslot2] = temp
	return 1

def check_teachers_empty_periods(to_file: int, 
		mode: int,
		begin: int,
		end: int,
		a: list,
		number_of_teachers1: int,
		TEPW1: float,
		show_results: int = 0
		): # checks the teacher's empty periods and returns the relevant cost
	total_cost = 0.0
	start = 0
	days = 0
	cases_of_teachers = 0

	total_gaps_of_teachers = 0

	if mode == 0:
		for i in range(number_of_teachers1):
			cost = 0.0
			total_gaps = 0
			days = 0

			for start in range(begin,end,7):
				gaps = 0
				teaching_hours = 0
				last_lesson = start
				first_lesson = start
				flag = 1
				has_lesson = 0

				for t in range(start,start+7):
					for j in range(teachers[i].num_of_classes):
						if (a[teachers[i].classes_he_teaches[j][0]][t] == i):
							has_lesson = 1
							if flag == 1:
								first_lesson = t
								flag = 0
							last_lesson = t
							teaching_hours += 1
							break

				if has_lesson == 1:
					gaps = last_lesson - first_lesson + 1 - teaching_hours
					total_gaps += gaps

				if gaps > 0:
					total_gaps_of_teachers += gaps
					days += 1

			if days > 0:
				cases_of_teachers += 1
				cost = TEPW1 * total_gaps * pow(BASE,days)

			if show_results == 1:
				print(f"Teacher {teachers[i].surname} has {days} days with total gaps: {total_gaps}")
			if to_file == 33:
				fp3.write(f"Teacher {teachers[i].surname} has {days} days with total gaps: {total_gaps}")

			total_cost += cost
		if show_results == 1 or show_results == 2:
			print(f"There are {cases_of_teachers} teachers with {total_gaps_of_teachers} total idle timeslots")
		if to_file == 33:
			fp3.write(f"There are {cases_of_teachers} teachers with {total_gaps_of_teachers} total idle timeslots")
			fp3.write(f"Empty teachers timeslot cost is {total_cost}")
		return total_cost

	for i in range(number_of_teachers1):
		cost = 0.0
		total_gaps = 0
		days = 0

		for start in range(begin,end,start+7):
			gaps = 0
			teaching_hours = 0
			last_lesson = start
			first_lesson = start
			flag = 1
			has_lesson = 0

			for t in range(start,start+7):
				for j in range(teachers[i].num_of_classes):
					class1 = teachers[i].classes_he_teaches[j][0]

					if teachers[i].kind == 0:
						if a[class1][t] == i:
							has_lesson = 1
							if flag == 1:
								first_lesson = t
								flag = 0
							last_lesson = t
							teaching_hours += 1
					else:
						co_class1 = co_class[class1][i]
						if co_class1 == class1:
							co_teacher1 = co_teacher[i][co_class1]
						else:
							co_teacher1 = 2015

						if co_teacher1 < 0:
							if a[class1][t] == i:
								has_lesson = 1
								if flag == 1:
									first_lesson = t
									flag = 0
								last_lesson = t
								teaching_hours += 1
						else:
							if a[class1][t] == i or a[class1][t] == co_teacher1:
								has_lesson = 1
								if flag == 1:
									first_lesson = t
									flag = 0
								last_lesson = t
								teaching_hours += 1
								break

			if has_lesson == 1:
				gaps = last_lesson - first_lesson + 1 - teaching_hours
				total_gaps += gaps
			if gaps > 0:
				total_gaps_of_teachers += gaps 
				days += 1

		if days > 0:
			cases_of_teachers += 1
			cost = TEPW1 * total_gaps * pow(BASE,days)

		if show_results == 1:
			print(f"Teacher {teachers[i].surname} has {days} days with total gaps: {total_gaps}")
		if to_file == 33:
			fp3.write(f"Teacher {teachers[i].surname} has {days} days with total gaps: {total_gaps}")

		total_cost += cost


	if show_results == 1 or show_results == 2:
		print(f"There are {cases_of_teachers} teachers with {total_gaps_of_teachers} total idle timeslots")
	if to_file == 33:
		fp3.write(f"There are {cases_of_teachers} teachers with {total_gaps_of_teachers} total idle timeslots")
		fp3.write(f"Empty teachers timeslot cost is {total_cost}")
	return total_cost

def calculate_ideal_teacher_dispersion(teacher11: int, total_hours1: int):
	return 7 * total_hours1 / float(teachers[teacher11].availability_hours)

