#from django.db import models

# Create your models here.

class TimeBlock:
	def __init__(self,
			label: str,
			M_start_time: str = None,
			M_end_time: str = None,
			T_start_time: str = None,
			T_end_time: str = None,
			W_start_time: str = None,
			W_end_time: str = None,
			H_start_time: str = None,
			H_end_time: str = None,
			F_start_time: str = None,
			F_end_time: str = None):
		self.label = label
		self.days = {
			"M": None,
			"T": None,
			"W": None,
			"H": None,
			"F": None
		}
		if M_start_time is not None and M_end_time is not None:
			days["M"] = {"start": M_start_time, "end": M_end_time}
		if T_start_time is not None and T_end_time is not None:
			days["T"] = {"start": T_start_time, "end": T_end_time}
		if W_start_time is not None and W_end_time is not None:
			days["W"] = {"start": W_start_time, "end": W_end_time}
		if H_start_time is not None and H_end_time is not None:
			days["H"] = {"start": H_start_time, "end": H_end_time}
		if F_start_time is not None and F_end_time is not None:
			days["F"] = {"start": F_start_time, "end": F_end_time}

	def changeTime(self, day, new_start: str = None, new_end: str = None):
		if new_start is None or new_end is None:
			self.days[day] = None
		else:
			self.days[day] = {"Start": new_start, "End": new_end}

	def getOutputDict(self):
		times = {}
		for k,v in self.days.items():
			if v is not None:
				times[k] = v
		return times

	def getLabel(self):
		return self.label

def getBlock(blocks: list[TimeBlock], label: str):
	for block in blocks:
		if block.getLabel == label:
			return block
	return -1

class Course:
	def __init__(self,
			course_name: str,
			course_size: int = 0,
			session: str = "",
			section: str = "A01",
			prof: str = "", #maybe change to a prof object in the future
			times: TimeBlock = None,
			classroom: str = "", #maybe change to a classroom object in the future
			prereqs: list = [],
			coreqs: list = [],
			core: bool = False
		): 
		self.course_name = course_name
		self.course_size = course_size
		self.session = session
		self.section = section
		self.prof = prof
		self.times = None
		self.classroom = classroom
		self.prereqs = prereqs
		self.coreqs = coreqs
		self.core = core


	# Directly change any field (except course name)
	def changeInfo(self,
			course_size: int = None,
			session: str = None,
			section: str = None,
			prof: str = None,
			times: TimeBlock = None,
			classroom: str = None,
			prereqs: list = None,
			coreqs: list = None,
			core: bool = None
		):
		if course_size is not None:
			self.course_size = course_size
		if session is not None:
			self.session = session
		if section is not None:
			self.section = section
		if prof is not None:
			self.prof = prof
		if times is not None:
			self.times = times
		if classroom is not None:
			self.classroom = classroom
		if prereqs is not None:
			self.prereqs = prereqs
		if coreqs is not None:
			self.coreqs = coreqs
		if core is not None:
			self.core = core

	def getSession(self):
		return self.session

	def addPrereq(self,new_prereq: str):
		self.prereqs.append(new_prereq)

	def addCoreq(self,new_coreq: str):
		self.coreqs.append(new_coreq)



	# Gets a dictionary containing information the scheduler needs to output
	def getOutputDict(self):
		out = {
			'Course': self.course_name,
			'Section': self.section,
			'Prof': self.prof,
			'Times': self.times.getOutputDict() if self.times is not None else "",
			'Class': self.classroom,
			'Course Size': self.course_size
		}
		return out

	# Copies course details to a different term
	# Use case: courses that are run by the same prof multiple semesters
	# returns the new Course object
	def cloneToSession(self, new_session: str):
		if new_session == self.session:
			return None
		return Course(
			course_name = self.course_name,
			course_size = self.course_size,
			session = new_session,
			prof = self.prof,
			times = self.times,
			classroom = self.classroom,
			prereqs = self.prereqs,
			coreqs = self.coreqs,
			core = self.core
			)

	# Adds another section for the same course.
	# Increments the section number if none is provided
	# same_info: copies the same info, used for lectures split into sections but still at the same time/room
	def addSection(self,
			new_section: str,
			same_info = False #,
		):

		if not new_section:
			new_section = self.section[0] + format(int(self.section[1:]) + 1, '02d')
		if same_info:
			return Course(
				course_name = self.course_name,
				course_size = self.course_size,
				session = self.session,
				section = new_section,
				prof = self.prof,
				times = self.times,
				classroom = self.classroom,
				prereqs = self.prereqs,
				coreqs = self.coreqs,
				core = self.core
				)
		
		return Course(course_name = self.course_name, session = self.session, section = new_section, core = self.core)
