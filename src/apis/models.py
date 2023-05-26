#from django.db import models

# Create your models here.

class Course:
	def __init__(self,
			course_name: str,
			course_size: int = 0,
			session: str = "",
			section: str = "A01",
			prof: str = "", #maybe change to a prof object in the future
			start_time: str = "",
			end_time: str = "",
			days: str = "", #maybe make a list?
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
		self.start_time = start_time
		self.end_time = end_time
		self.days = days
		self.classroom = classroom
		self.prereqs = prereqs
		self.coreqs = coreqs
		self.core = core


	# Directly change any field (except course name)
	def changeInfo(
			course_size: int = None,
			session: str = None,
			section: str = None,
			prof: str = None,
			start_time: str = None,
			end_time: str = None,
			days: str = None,
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
			self.section = new_section
		if prof is not None:
			self.prof = prof
		if start_time is not None:
			self.start_time = start_time
		if end_time is not None:
			self.end_time = end_time
		if days is not None:
			self.days = days
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

	def addPrereq(new_prereq: str):
		self.prereqs.append(new_prereq)

	def addCoreq(new_coreq: str):
		self.coreqs.append(new_coreq)

	# Gets a dictionary containing information the scheduler needs to output
	def getOutputDict(self):
		out = {
			'Course': self.course_name,
			'Section': self.section,
			'Prof': self.prof,
			'Start Time': self.start_time,
			'End Time': self.end_time,
			'Days': self.days,
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
			start_time = self.start_time,
			end_time = self.end_time,
			days = self.days,
			classroom = self.classroom,
			prereqs = self.prereqs,
			coreqs = self.coreqs,
			core = self.core
			)

	# Adds another section for the same course.
	# Increments the section number if none is provided
	# same_info: copies the same info, used for lectures split into sections but still at the same time/room
	def addSection(self,
			new_section: str = None,
			same_info = False #,
		):

		if not new_section:
			new_section = self.section[0] + format(int(section[1:]) + 1, '02d')
		if same_info:
			return Course(
				course_name = self.course_name,
				course_size = self.course_size,
				session = self.session,
				section = new_section,
				prof = self.prof,
				start_time = self.start_time,
				end_time = self.end_time,
				days = self.days,
				classroom = self.classroom,
				prereqs = self.prereqs,
				coreqs = self.coreqs,
				core = self.core
				)
		
		return Course(course_name = self.course_name, session = self.session, section = new_section, core = self.core)

