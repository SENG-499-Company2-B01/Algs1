
import random
import datetime
import math
import time

#declarations of file names
fp = None
fp1 = None
fp2 = None
fp3 = None
fp4 = None

# definitions of variables and constants
class_name_length = 15 # maximum length of a class's name
class_name = ['' for x in range (class_name_length)] 
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
			available_days: int = 0,
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
		self.available_days = available_days
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
			class_name: str = '',
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

def swap(a:list, class1: int, timeslot1: int, timeslot2: int):
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

def calculate_floor_ceil_number(floor_no: int, ceil_no: int, teacher11: int, total_hours1: int) -> int:
	ideal = calculate_ideal_teacher_dispersion(teacher11, total_hours1)
	floor1 = math.floor(ideal)
	ceil_no = total_hours1 % teachers[teacher11].available_days

	if floor1 == 0:
		floor_no = 0
	else:
		floor_no = teachers[teacher11].available_days - ceil_no
	
	return 1

# returns the total number (including co-teachings) of teaching hours of teacher
def find_implied_and_actual_hours_of_teacher(teacher1: int, number_of_teachers1: int):
	implied_hours_of_teacher = 0

	if teachers[teacher1].kind == 0:
		return teachers[teacher1].total_hours
	
	for t in range(0, number_of_teachers1):
		if teachers[t].count_of_coteachers == 0:
			continue
		for z in range(0, teachers[t].count_of_coteachers):
			if ((teachers[t].coteachings[z][0] == teacher1) and (teachers[t].coteachings[z][3] == teachers[t].coteachings[z][4])):
				class1 = teachers[t].coteachings[z][3]

				for c in range(0, teachers[teacher1].num_of_classes):
					class2 = teachers[teacher1].classes_he_teaches[c][0]

					if ((teachers[teacher1].classes_he_teaches[c][1] == 0) and (class2 == class1)):
						implied_hours_of_teacher = implied_hours_of_teacher + teachers[t].coteachings[z][1]

	teachers[teacher1].total_hours = teachers[teacher1].total_hours + implied_hours_of_teacher

	return teachers[teacher1].total_hours

def check_teachers_dispersion(to_file: int, begin: int, end: int, a: list, number_of_teachers1: int, IDTW: float, show_results: int):# checks the dispersion of teaching hours of the teacher and returns the relevant cost
	start = 0
	ceil_no = 0
	floor_no = 0
	absolute_error = 0.0
	total_cost = 0.0
	totalNumberOfWrongTeachers = 0
	total_fault_days = 0
	actualDistTable = []
	idealDistrTable = []

	for i in range(0, number_of_teachers1):
		absolute_error = 0.0
		ideal = calculate_ideal_teacher_dispersion(i, teachers[i].total_hours)
		calculate_floor_ceil_number(floor_no, ceil_no, i, teachers[i].total_hours)

		for start in range(begin, end, 7):
			hours_per_day = 0

			for j in range(0, teachers[i].num_of_classes):
				hours_per_day_of_class = 0
				class1 = teachers[i].classes_he_teaches[j][0]
				co_class1 = co_class[class1][i]

				if co_class1 == class1:
					co_teacher1 = co_teacher[i][co_class1]
				else:
					co_teacher1 = 2015

				for t in range(start, start + 7):
					if teachers[i].kind == 0:
						if a[class1][t] == i:
							hours_per_day_of_class = hours_per_day_of_class + 1
					else:
						if co_teacher1 < 0:
							if a[class1][t] == i:
								hours_per_day_of_class = hours_per_day_of_class + 1

						else:
							if a[class1][t] == co_teacher1 or a[class1][t] == i:
								hours_per_day_of_class = hours_per_day_of_class + 1

				hours_per_day = hours_per_day + hours_per_day_of_class

			actualDistTable[start / 7] = hours_per_day	

		for j in range(0, 5):
			if teachers[i].is_available_at_day[j] == -1:
				idealDistrTable[j] = -1
				continue
			else:
				if floor_no > 0:
					idealDistrTable[j] = math.floor(ideal)
					floor_no = floor_no - 1
					continue
				if ceil_no > 0:
					idealDistrTable[j] = math.ceil(ideal)
					ceil_no = ceil_no - 1
					continue
				if floor_no == 0 and ceil_no == 0:
					idealDistrTable[j] = 0
					continue
		
		for ii in range(0, 5):
			for j in range(0, 5):
				if actualDistTable[ii] == 0 and idealDistrTable[j] == -1 and ii == j:
					actualDistTable[ii] = -2
					idealDistrTable[j] = -2
					break
				if actualDistTable[ii] == idealDistrTable[j]:
					actualDistTable[ii] = -2
					idealDistrTable[j] = -2
					break
		
		faultDays = 0
		for ii in range(0, 5):
			if actualDistTable[ii] == -2:
				continue
			diff1 = 50
			diff2 = 100

			index = -1
			for j in range(0, 5):
				if idealDistrTable[j] == -2:
					continue
				if idealDistrTable[j] == -1:
					idealDistrTable[j] = 0
				diff2 = abs(actualDistTable[ii] - idealDistrTable[j])
				if diff2 < diff1:
					diff1 = diff2
					index = j
			
			if diff1 != 0:
				absolute_error = absolute_error + diff1
				faultDays = faultDays + 1
				idealDistrTable[index] = -2

		if faultDays > 0:
			cost = absolute_error * pow(BASE, float(faultDays))
			total_fault_days = total_fault_days + faultDays
			total_cost = total_cost + cost
			totalNumberOfWrongTeachers = totalNumberOfWrongTeachers + 1

			if show_results == 1:
				print("\nTeacher %s has %d days with wrong dispersion\n", teachers[i].surname, faultDays)
				print("-----------------------------------------------------------------------------\n")
			
			if to_file == 33:
				print("\nTeacher %s has %d days with wrong dispersion\n", teachers[i].surname, faultDays, file=open('fp3', 'a'))
				print("-----------------------------------------------------------------------------\n", file=open('fp3', 'a'))
	
	if show_results == 1 or show_results == 2:
		print("Total cases of Teachers wrong dispersion are %d. The number of these days are %d\n", totalNumberOfWrongTeachers, total_fault_days)

	if to_file == 33:
		print("\nTotal cases of Teachers wrong dispersion are %d. The number of these days are %d\n", totalNumberOfWrongTeachers, total_fault_days, file=open('fp3', 'a'))
		print("\nWrong teacher dispersion cost is %.12f\n", IDTW * total_cost, file=open('fp3', 'a'))
	
	return IDTW * total_cost


# checks the dispersion of lessons of each class and returns the relevant cost

def check_classes_dispersion(to_file: int, begin: int, end: int, a: list, number_of_classes1: int, ICDW1: float, show_results: int) -> float:
	i, k, start, t, hours_per_day_of_teacher, problem_days, violation_cases: int
	hours, total_hours_per_class, total_problem_days, co_class1, co_teacher1, teacher1, jj: int
	cost, total_cost:float = 0.0
	index1 = 0
	violation_cases = 0
	total_problem_days = 0

	for i in range(0, number_of_classes1):		
		problem_days = 0
		cost = 0.0
		total_hours_per_class = 0
		for start in range(begin, end, 7):
			hours = 0
			for k in range(0, classes[i].number_of_teachers):
				hours_per_day_of_teacher = 0
				teacher1 = classes[i].teachers_of_class_and_hours[k][0]
				co_class1 = co_class[i][teacher1]
				if co_class1 == i:
					co_teacher1 = co_teacher[teacher1][co_class1]
				else:
					co_teacher1 = 2015
				
				for t in range(start, start + 7):
					if (a[i][t] == teacher1 and co_class1 == -1) or (a[i][t] == co_teacher1):
						hours_per_day_of_teacher = hours_per_day_of_teacher + 1
				
				if classes[i].teachers_of_class_and_hours[k][2] > 0 and hours_per_day_of_teacher > classes[i].teachers_of_class_and_hours[k][2]:
					hours = hours + hours_per_day_of_teacher - classes[i].teachers_of_class_and_hours[k][2]
				elif classes[i].teachers_of_class_and_hours[k][2] == 0:
					for jj in range(0, classes[i].number_of_teachers):
						if classes[i].teachers_of_class_and_hours[jj][0] == co_teacher1:
							break
					if hours_per_day_of_teacher > classes[i].teachers_of_class_and_hours[jj][2]:
						hours = hours + hours_per_day_of_teacher - classes[i].teachers_of_class_and_hours[k][2]


			if hours > 0:
				total_hours_per_class = total_hours_per_class + hours
				problem_days = problem_days + 1

		if problem_days > 0:
			total_problem_days = total_problem_days + problem_days
			violation_cases = violation_cases + 1
			index1 = index1 + 1

			cost = ICDW1 * total_problem_days * pow(BASE, problem_days)

			if show_results == 1:
				print("\nThe class %s has %d repeated lessons at %d  days\n", classes[i].class_name, total_hours_per_class, problem_days)
				print("---------------------------------------------------------------------------------\n")
			
			if to_file == 33:
				print("\nThe class %s has %d repeated lessons at %d  days\n", classes[i].class_name, total_hours_per_class, problem_days, file=open('fp3', 'a'))
				print("---------------------------------------------------------------------------------\n", file=open('fp3', 'a'))
			
		total_cost = total_cost + cost
	
	if show_results == 1 or show_results == 2:
		print("The classes with  wrong dispersion are %d. The days it occurs are %d\n", violation_cases, total_problem_days)
			
	if to_file == 33:
		print("\nThe classes with  wrong dispersion are %d. The days it occurs are %d\n", violation_cases, total_problem_days, file=open('fp3', 'a'))
		print("\nWrong class dispersion cost is %.12f\n", total_cost, file=open('fp3', 'a'))
	
	return total_cost	

def check_parallel_teaching(to_file: int,
		mode: int,
		start: int,
		end: int,
		a: list,
		number_of_teachers1: int,
		number_of_classes1: int,
		show_results: int): #checks if there are parallel teachings and returns the relevant cost
	number_of_cases = 0
	cost = 0.0

	if mode == 0:
		for i in range(number_of_teachers1):
			for t in range(start,end):
				parallel_teaching = 0
				for j in range(number_of_classes1):
					if a[j][t] == i:
						parallel_teaching += 1
				if parallel_teaching > 1:
					number_of_cases += 1
					cost += HCW*pow(BASE,parallel_teaching - 1)

		if show_results == 1:
			print(f"Total cases of teacher parallel teaching are {number_of_cases}")
		if to_file == 33:
			fp3.write(f"Total cases of teacher parallel teaching is {number_of_cases}")
		return cost

	for i in range(number_of_teachers1):
		for t in range(start,end):
			parallel_teaching = 0

			for j in range(number_of_classes1):
				if teachers[i].kind == 0:
					if a[j][t] == i:
						parallel_teaching += 1
					else:
						co_class1 = co_class[j][i]
						if co_class1 == j:
							co_teacher1 = co_teacher[i][co_class1]
						else:
							co_teacher1 = 2015
						if co_teacher1 < 0:
							if a[j][t] == i:
								parallel_teaching += 1
							else:
								if a[j][t] == i or a[j][t] == co_teacher1:
									parallel_teaching += 1

			if parallel_teaching > 1:
				number_of_cases += 1
				cost += HCW * pow(BASE,parallel_teaching - 1)

	if show_results == 1:
		print(f"Total cases of teacher parallel teaching are {number_of_cases}")
	if to_file == 33:
		fp3.write(f"Total cases of teacher parallel teaching is {number_of_cases}")
		fp3.write(f"Parallel teaching cost is {cost}")
	return cost

def check_class_empty_periods(to_file: int,
			begin: int,
			end: int,
			a: list,
			number_of_classes1: int,
			show_results: int): # checks the empty periods of each class and returns the relevant cost
	number_of_cases = 0
	cost = 0.0

	for i in range(number_of_classes1):
		for start in range(begin, end, 7):
			for t in range(start, start+7):
				if a[i][t] == -1 and t != 6 and t != 13 and t != 20 and t != 27 and t != 34:
					number_of_cases += 1
					cost += HCW*pow(2*BASE,BASE)

					if show_results == 1:
						print(f"Class {classes[i].class_name} has empty timeslot {t}")
					if to_file == 33:
						fp3.write(f"Class {classes[i].class_name} has empty timeslot {t}")

	if show_results == 1:
		print(f"Total cases of class empty periods are {number_of_cases}")

	if to_file == 33:
		fp3.write(f"Total cases of class empty periods are {number_of_cases}")
		fp3.write(f"Total cost of empty class timeslots is {cost}")
	return cost

def check_teacher_unavailability(to_file: int,
			mode: int,
			start: int,
			end: int,
			a: list,
			number_of_classes1: int,
			show_results: int): # checks the unavailability of each teacher and returns the relevant cost
	number_of_cases = 0
	cost = 0.0
	if mode == 0:
		for i in range(number_of_classes1):
			for j in range(classes[i].number_of_teachers):
				for t in range(start,end):
					if a[i][t] == classes[i].teachers_of_class_and_hours[j][0] and teachers[classes[i].teachers_of_class_and_hours[j][0]].unavailable_timeslots[t] == 1:
						number_of_cases += 1
		cost = number_of_cases * HCW * pow(BASE< 4.75)
		if show_results == 1:
			print(f"Total cases of teacher unavailability are {number_of_cases}")
		if to_file == 33:
			fp3.write(f"Total cases of teacher unavailability {number_of_cases}")
		return cost

	for i in range(number_of_classes1):
		for j in range(classes[i].number_of_teachers):
			first_teacher = classes[i].teachers_of_class_and_hours[j][0]

			for t in range(start,end):
				if teachers[first_teacher].kind == 0:
					if first_teacher == a[i][t] and teachers[first_teacher].unavailable_timeslots[t] == 1:
						number_of_cases += 1
				else:
					co_class1 = co_class[i][first_teacher]
					if co_class1 == i:
						co_teacher1 = co_teacher[first_teacher][co_class1]

					if co_class1 == i:
						co_teacher1 = co_teacher[first_teacher][co_class1]
					else:
						co_teacher1 = 2015

					if co_teacher1 < 0:
						if first_teacher == a[i][t] and teachers[first_teacher].unavailable_timeslots[t] == 1:
							number_of_cases += 1
						elif co_teacher1 == 2015:
							if first_teacher == a[i][t] and teachers[first_teacher].unavailable_timeslots[t] == 1:
								number_of_cases += 1
						elif co_teacher1 > 0 and co_teacher1 != 2015:
							if co_teacher1 == a[i][t] and teachers[first_teacher].unavailable_timeslots[t] == 1:
								number_of_cases += 1

	cost = number_of_cases * HCW * pow(BASE,3)

	if show_results == 1:
		print(f"Total cases of teacher unavailability are {number_of_cases}")
	if to_file == 33:
		fp3.write(f"Total cases of teacher unavailability: {number_of_cases}")
		fp3.write(f"Unavailability cost is {cost}")

	return cost

def check_validity(mode: int,
			begin: int,
			end: int,
			a: list,
			class1: int,
			number_of_teachers: int,
			number_of_classes: int,
			timeslot1: int,
			timeslot2: int,
			TEPW1: float): # checks if there are hard constraint violations in a swap made during the optimization phase
	if a[class1][timeslot1] == -1 and a[class1][timeslot2] == -1:
		return 1

	if teachers[a[class1][timeslot1]].unavailable_timeslots[timeslot2] == 1 or teachers[a[class1][timeslot2]].unavailable_timeslots[timeslot1] == 1:
		return -1

	if mode == 1:
		class2 = co_class[class1][a[class1][timeslot1]]
		second_teacher = co_teacher[a[class1][timeslot1]][class1]

		if second_teacher < 0 and teachers[-second_teacher].unavailable_timeslots[timeslot2] == 1:
			return -1

		if second_teacher != 2015 and teachers[second_teacher].unavailable_timeslots[timeslot2] == 1:
			return -1

		class2 = co_class[class1][a[class1][timeslot2]]
		second_Teacher = co_teacher[a[class1][timeslot2]][class1]

		if second_teacher < 0 and teachers[-second_teacher].unavailable_timeslots[timeslot2] == 1:
			return -1

		if second_teacher != 2015 and teachers[second_teacher].unavailable_timeslots[timeslot2] == 1:
			return -1

	ok3 = check_parallel_teaching(0,mode,begin,end,a,number_of_teachers,number_of_classes,0)
	swap(a,class1,timeslot1,timeslot2)

	ok4 = check_parallel_teaching(0,mode,begin,end,a,number_of_teachers,number_of_classes,0)

	if ok4 > ok3:
		swap(a,class1,timeslot1,timeslot2)
		return -1
	else:
		swap(a,class1,timeslot1,timeslot2)

	ok3 = check_class_empty_periods(0,begin,end,a,number_of_classes,0)
	swap(a,class1,timeslot1,timeslot2)
	ok4 = check_class_empty_periods(0,begin,end,a,number_of_classes,0)

	if ok4 > ok3:
		swap(a,class1,timeslot1,timeslot2)
		return -1
	else:
		swap(a,class1,timeslot1,timeslot2)

	swap_done = 0

	ok3 = check_wrong_coteaching(0,begin,end,a,number_of_classes,0)

	if teachers[a[class1][timeslot1]].kind == 1:
		swap(a,class1,timeslot1,timeslot2)
		class2 = co_class[class1][a[class1][timeslot1]]
		second_teacher = co_teacher[a[class1][timeslot1]][class1]

		if (class2 != -1 and a[class2][timeslot1] == second_teacher) or (second_teacher < 0 and a[class2][timeslot1] == -second_teacher):
			swap(a, class2, timeslot1, timeslot2)
			swap_done = 1
	else:
		swap(a,class1,timeslot1,timeslot2)

	ok4 = check_wrong_coteaching(0,begin,end,a,number_of_classes,0)

	if ok4 > ok3:
		swap(a, class1, timeslot1, timeslot2)
		if teachers[a[class1][timeslot1]].kind == 1:
			if swap_done == 1:
				swap(a,class2,timeslot1,timeslot2)
		return -1
	else:
		swap(a,class1,timeslot1,timeslot2)
		if teachers[a[class1][timeslot1]].kind == 1:
			if swap_done == 1:
				swap(a,class2,timeslot1,timeslot2)
	f1 = check_teachers_empty_periods(0,mode,begin,end,a,number_of_teachers,TEPW1,0)

	swap(a,class1,timeslot1,timeslot2)

	f2 = check_teachers_empty_periods(0,mode,begin,end,a,number_of_teachers,TEPW1, 0)

	if f2 > f1:
		swap(a, class1,timeslot1,timeslot2)
		return -2
	else:
		swap(a,class1,timeslot1,timeslot2)
	return 1

def accept_swap(mode: int,
			begin: int,
			end: int,
			a: list,
			class1: int,
			teachers_number: int,
			number_of_classes: int,
			timeslot1: int,
			timeslot2: int,
			TEPW1: float): # approves or rejects a swap during the optimization phase
	ok = check_validity(mode,begin,end,a,class1,teachers_number,number_of_classes,timeslot1,timeslot2,TEPW1)

	if ok == 1:
		return 1
	elif ok == -1:
		r1 = random.randint(0,2147483647)/(2147483647+1.0)

		if r1 <= 1/92: # in order to improve the diversity of the results, swaps with hard constraint violations are rarely accepted
			return 1 
		return -1
	elif ok == -1:
		return -1
	return -1

def perform_swap(mode: int,
			begin: int,
			end: int,
			a: list,
			timeslot1: int,
			timeslot2: int,
			class_no1: int,
			teachers_number: int,
			TEPW1: float): # performs a swap during the optimization phase
	for i in range(class_no1):
		ok = accept_swap(mode,begin,end,a,i,teachers_number,class_no1,timeslot1,timeslot2,TEPW1)

		if ok == 1:
			swap(a,i,timeslot1,timeslot2)

			if teachers[a[i][timeslot1]].kind == 1:
				co_class1 = co_class[i][a[i][timeslot1]]
				co_teacher1 = co_teacher[a[i][timeslot1]][i]

				if co_class1 != -1 and ((co_teacher1 < 0 and a[co_class1][timeslot1] == -co_teacher1) or (co_teacher1 > 0 and a[co_class1][timeslot1] == co_teacher1)):
					swap(a,co_class1,timeslot1,timeslot2)

	return 1

# copies the contents of a matrix
def copy_matrices(begin: int, end: int, destination: list, source: list, dim: int):
	i, j: int
	for i in range(0, dim):
		for j in range(begin, end):
			destination[i][j] = source[i][j]

# Calculates the fitness value
def calculate_fitness(mode, start, end, a, number_of_teachers, number_of_classes, TEPW, ITDW, ICDW):
	a1 = check_teacher_unavailability(0, mode, start, end, a, number_of_classes, 0)
	a2 = check_parallel_teaching(0, mode, start, end, a, number_of_teachers, number_of_classes, 0)
	a3 = check_class_empty_periods(0, start, end, a, number_of_classes, 0)
	a4 = check_wrong_coteaching(0, start, end, a, number_of_classes, 0)
	a5 = check_teachers_empty_periods(0, mode, start, end, a, number_of_teachers, TEPW, 0)
	a6 = check_teachers_dispersion(0, start, end, a, number_of_teachers, ITDW, 0)
	a7 = check_classes_dispersion(0, start, end, a, number_of_classes, ICDW, 0)
	return a1 + a2 + a3 + a4 + a5 + a6 + a7

# calculates the fitness value without the costs of teachers' and classes' dispersion
def calculate_partial_fitness(mode, start, end, a, number_of_teachers, number_of_classes, TEPW):
	a1 = check_teacher_unavailability(0, mode, start, end, a, number_of_classes, 0)
	a2 = check_parallel_teaching(0, mode, start, end, a, number_of_teachers, number_of_classes, 0)
	a3 = check_class_empty_periods(0, start, end, a, number_of_classes, 0)
	a4 = check_wrong_coteaching(0, start, end, a, number_of_classes, 0)
	a5 = check_teachers_empty_periods(0, mode, start, end, a, number_of_teachers, TEPW, 0)
	return a1 + a2 + a3 + a4 + a4 + a5

# calculates the fitness value only for the hard constraints
def check_hard_constraints(mode, start, end, a, number_of_teachers, number_of_classes):
	a1 = check_teacher_unavailability(0, mode, start, end, a, number_of_classes, 0)
	a2 = check_parallel_teaching(0, mode, start, end, a, number_of_teachers, number_of_classes, 0)
	a3 = check_class_empty_periods(0, start, end, a, number_of_classes, 0)
	a4 = check_wrong_coteaching(0, start, end, a, number_of_classes, 0)
	return a1 + a2 + a3 + a4 + a4

def display_results(to_file: int,
		mode: int,
		begin: int,
		end: int,
		a: list,
		number_of_teachers1: int,
		number_of_classes1: int,
		TEPW1: float,
		ITDW1: float,
		ICDW1: float): # displays the results
	if to_file == 4:
		print("\n\nRESULTS BEFORE OPTIMIZATION\n----------------\nHard constraints")

		a1 = check_teacher_unavailability(to_file,mode,begin,end,a,number_of_classes1,1)
		a2 = check_parallel_teaching(to_file,mode,begin,end,a,number_of_teachers1,number_of_classes1,1)
		a3 = check_class_empty_periods(to_file,begin,end,a,number_of_classes1,1)
		a4 = check_wrong_coteaching(to_file,begin,end,a,number_of_classes1,1)

		print("\nSoft constraints\n")

		a5 = check_teachers_dispersion(to_file,begin,end,a,number_of_teachers1,ITDW1,2)
		a6 = check_classes_dispersion(to_file,begin,end,a,number_of_classes1,ICDW1,2)
		a7 = check_teachers_empty_periods(to_file,mode,begin,end,a,number_of_teachers1,TEPW1,2)
		return

	if to_file == 33:
		fp3.print("RESULTS ANALYSIS\n----------------\n")

	print("\n\nRESULTS BEFORE OPTIMIZATION\n----------------\nHard constraints")
	a1 = check_teacher_unavailability(to_file,mode,begin,end,a,number_of_classes1,1)
	a2 = check_parallel_teaching(to_file,mode,begin,end,a,number_of_teachers1,number_of_classes1,1)
	a3 = check_class_empty_periods(to_file,begin,end,a,number_of_classes1,1)
	a4 = check_wrong_coteaching(to_file,begin,end,a,number_of_classes1,1)

	print("\nSoft constraints\n")

	a5 = check_teachers_dispersion(to_file,begin,end,a,number_of_teachers1,ITDW1,2)
	a6 = check_classes_dispersion(to_file,begin,end,a,number_of_classes1,ICDW1,2)
	a7 = check_teachers_empty_periods(to_file,mode,begin,end,a,number_of_teachers1,TEPW1,2)

	if to_file == 3:
		print(f"\nCOST SUMMARY (as calculated for TEPW={TEPW1}, ICDW={ICDW1}, ITDW={ITDW1})")
		print("-------------------------------------------------------------------")
		print(f"Cost of unavailability : {a1}")
		print(f"Cost of parallel teaching : {a2}")
		print(f"Cost of class empty periods : {a3}")
		print(f"Cost of wrong co-teaching : {a4}")
		print(f"Cost of teachers dispersion : {a5}")
		print(f"Cost of class dispersion : {a6}")
		print(f"Cost of teachers empty periods : {a7}")
		print(f"T o t a l   c o s t   i s   {a1+a2+a3+a4+a5+a6+a7}")
	elif to_file == 3:
		fp3.write(f"\nCOST SUMMARY (as calculated for TEPW={TEPW1}, ICDW={ICDW1}, ITDW={ITDW1})")
		fp3.write("-------------------------------------------------------------------")
		fp3.write(f"Cost of unavailability : {a1}")
		fp3.write(f"Cost of parallel teaching : {a2}")
		fp3.write(f"Cost of class empty periods : {a3}")
		fp3.write(f"Cost of wrong co-teaching : {a4}")
		fp3.write(f"Cost of teachers dispersion : {a5}")
		fp3.write(f"Cost of class dispersion : {a6}")
		fp3.write(f"Cost of teachers empty periods : {a7}")
		fp3.write(f"T o t a l   c o s t   i s   {a1+a2+a3+a4+a5+a6+a7}")
	return

# locates the data of a co-teaching
def display_implied_teacher(teacher3: int, class3: int, coteacher: int, coclass: int, locate_coteacher: int, number_of_teachers1: int):
	t, z, class1, class2: int
	locate_coteacher = -2

	for t in range(0, number_of_teachers1):
		if teachers[t].count_of_coteachers == 0:
			continue
		for z in range(0, teachers[t].count_of_coteachers):
			if teachers[t].coteachings[z][0] == teacher3:
				class1 = teachers[t].coteachings[z][3]
				class2 = teachers[t].coteachings[z][4]

				if class1 == class2 and class1 == class3:
					coteacher = t
					coclass = class3
					locate_coteacher = 1
					return
				elif class1 != class2:
					if class3 == class1:
						coteacher = t
						coclass = class2
						locate_coteacher = -1
						return
					if class3 == class2:
						coteacher = t
						coclass = class1
						locate_coteacher = -1
						return
					continue

# -------------------- CSO FUNCTIONS --------------------
# -------- for more information consult the paper -------
# swaps two timeslots under certain conditions
def single_swap(a: list,timeslot1: int,timeslot2: int,class_num: int,classes_no: int):
	i, co_class1, co_teacher1=0,0,0
 
	if (timeslot1 == timeslot2):
		return -1
	if (a[class_num][timeslot1] == a[class_num][timeslot2]):
		return -1
	if (a[class_num][timeslot1] == -1 or a[class_num][timeslot2] == -1):
		return -1
    
	for i in range(classes_no):
		if (a[i][timeslot1] == a[class_num][timeslot2]):
			return -1
		if (a[i][timeslot2] == a[class_num][timeslot1]):
			return -1

	swap(a, class_num, timeslot1, timeslot2)
 
	if (teachers[a[class_num][timeslot1]].kind == 1):
		co_class1 = co_class[class_num][a[class_num][timeslot1]]
		co_teacher1 = co_teacher[a[class_num][timeslot1]][class_num]
		if (co_class1 != -1 and ((co_teacher1 < 0 and a[co_class1][timeslot1] == -co_teacher1) or (co_teacher1 > 0 and a[co_class1][timeslot1] == co_teacher1))):
			swap(a, co_class1, timeslot1, timeslot2)
	return 1

#replaces all the lessons in a timeslot of a cat with the ones in the same timeslot of another cat
def insert_column(mode: int,begin: int,end: int,source: list,destination: list,column: int ,class_no1: int,teachers_no :int,TEPW: float,ITDW: float,ICDW: float):
	i, j, jj, temp= 0,0,0,0
	aux=[0 for i in range(21)]
	store_positions_and_fitness=[[0 for k in range(21)] for i in range(2)]
	ff, smaller_fitness=0,0
	index, z, skip= 0,0,0
 
	for i in range(class_no1):
		if ((column == 6 or column == 13 or column == 20 or column == 27 or column == 34) and destination[i][column] == -1):
			continue
		if (destination[i][column] == source[i][column]):
			continue
		jj = 0
		j=begin
  
		while (j < end):
			if (destination[i][j] == source[i][column] and j != column):
				aux[jj] = j
				jj=jj+1
			j=j+1
		skip = 0
  
		for z in range(jj):
      
			if (aux[z] == column):
				skip = 1
				continue

			SwapInt(destination[i][aux[z]], destination[i][column], temp)
			ff = calculate_fitness(mode, 0, 35, destination, teachers_no, class_no1, TEPW, ITDW, ICDW)
   
			if (skip == 0):
				store_positions_and_fitness[0][z] = aux[z]
				store_positions_and_fitness[1][z] = ff
			else:
				store_positions_and_fitness[0][z - 1] = aux[z]
				store_positions_and_fitness[1][z - 1] = ff
    
			SwapInt(destination[i][aux[z]], destination[i][column],temp)
   
		smaller_fitness = inf
		index = 0
  
		for z in range(jj):
			if (store_positions_and_fitness[1][z] < smaller_fitness):
				smaller_fitness = store_positions_and_fitness[1][z]
				index = z
		SwapInt(destination[i][aux[index]], destination[i][column], temp)
  
#initializes the population of cats
def initialize_cats(classes_number: int,cat_number: int):
	i, j, k, p, class1, timeslot=0,0,0,0,0,0
 
	for p in range(cat_number):
		for j in range(classes_number):
			for i in range(classes[j].number_of_teachers):
				for k in range(3):
					classes[j].teachers_of_class_and_hours_remaining[i][k] = classes[j].teachers_of_class_and_hours[i][k]

		for class1 in range(classes_number):
			for timeslot in range(35):
				x[p][class1][timeslot] = -1

			for i in range(classes[class1].number_of_teachers):
				while (classes[class1].teachers_of_class_and_hours_remaining[i][1] > 0):
					timeslot = randint(0, 34)
					if (x[p][class1][timeslot] == -1):
						x[p][class1][timeslot] = classes[class1].teachers_of_class_and_hours[i][0]
						classes[class1].teachers_of_class_and_hours_remaining[i][1]=classes[class1].teachers_of_class_and_hours_remaining[i][1]-1
      
		for j in range(classes_number):
			for i in range(classes[j].number_of_teachers):
				for k in range(3):
					classes[j].teachers_of_class_and_hours_remaining[i][k] = classes[j].teachers_of_class_and_hours[i][k]
     
#cat seek procedure
def cat_seek(x: list,classes_no: int,teachers_no: int,TEPW: float,ITDW: float,ICDW: float):
	j, aa, bb, consider, cp, swaps_to_make, timeslots_to_change=0,0,0,0,0,0,0
	hd = []
	cn, tt1, tt2=0,0,0
	fs = []
	cfs = []
	tfs, fsmax, fsmin=0.0,0.0,0.0
	sl = []
	cat_copy = []
	temp_cat = []
	temp_cat1 = []
	all_equal = 0
	selected_copy = 0
	ll, best_fs, tmp1 = 0.0, 0.0, 0.0
	sel_prob = []
 
	best_fs = calculate_fitness(there_is_coteaching, 0, 35, x, teachers_no, classes_no, TEPW, ITDW, ICDW)
 
	if (SPC == 1):
		consider = 1
	else:
		consider = 0
  
	for cp in range(SMP):
		copy_matrices(0, 35, cat_copy[cp], x, classes_no)
  
	timeslots_to_change = int((CDC / 100.0) * 35.0)
 
	if (timeslots_to_change == 0):
		timeslots_to_change = 1
  
	swaps_to_make = int((SRD / 100.0) * classes_no * 35)
 
	for cp in range(SMP):
		copy_matrices(0, 35, temp_cat, cat_copy[cp], classes_no)

		if ((consider == 0) or ((consider == 1) and (cp != SMP - 1))):
			unique_randint(hd, 0, 34, timeslots_to_change)
   
			for aa in range(timeslots_to_change):
				insert_column(there_is_coteaching, 0, 35, global_best, temp_cat, hd[aa], classes_no, teachers_no, TEPW, ITDW, ICDW)
    
			copy_matrices(0, 35, temp_cat1, temp_cat, classes_no)
			unique_randint(sl, 0, (classes_no * 35) - 1, swaps_to_make)
   
			for bb in range(swaps_to_make):
				cn = int(sl[bb] / 35)
				tt1 = sl[bb] % 35
				tt2 = randint(0, 34)
    
				if (single_swap(temp_cat, tt1, tt2, cn, classes_no) != -1):
					tfs = calculate_fitness(there_is_coteaching, 0, 35, temp_cat, teachers_no, classes_no, TEPW, ITDW, ICDW)
     
					if (tfs <= best_fs):
						best_fs = tfs
						fs[cp] = tfs
						cfs[cp] = tfs
						copy_matrices(0, 35, cat_copy[cp], temp_cat, classes_no)
      
					copy_matrices(0, 35, temp_cat, temp_cat1, classes_no)
     
		else:
			fs[cp] = calculate_fitness(there_is_coteaching, 0, 35, cat_copy[cp], teachers_no, classes_no, TEPW, ITDW, ICDW)
			cfs[cp] = fs [cp]

	for i in range(SMP):
		j=1
		while (j < SMP):
			if (cfs[j] < cfs[j - 1]):
				ll = cfs[j - 1]
				cfs[j - 1] = cfs[j]
				cfs[j] = ll
			j=j+1
   
	fsmax = cfs[SMP - 1]
	fsmin = cfs[0]
 
	if (fsmax == fsmin):
		all_equal = 1
  
	if (all_equal == 1):
		selected_copy = randint(0, SMP - 1)
		copy_matrices(0, 35, x, cat_copy[selected_copy], classes_no)
  
	else:
		for i in range(SMP):
			sel_prob[i] = abs(fs[i] - fsmax) / (fsmax - fsmin)
   
		tmp1 = randd(0.0, 1.0)
  
		for i in range(SMP):
			if (tmp1 <= sel_prob[i]):
				copy_matrices(0, 35, x, cat_copy[i], classes_no)
