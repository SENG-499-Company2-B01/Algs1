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

	def changeInfo(self,
			new_course_size = None,
			new_session: str = '',
			new_section: str = '',
			new_prof: str = '',
			new_start_time: str = '',
			new_end_time: str = '',
			new_days: str = '',
			new_classroom: str = '',
			new_prereqs: list = [],
			new_coreqs: list = [],
			new_core = None
		):
		if new_course_size:
			self.course_size = new_course_size
		if new_session:
			self.session = new_session
		if new_section:
			self.section = new_section
		if new_prof:
			self.prof = new_prof
		if new_start_time:
			self.start_time = new_start_time
		if new_end_time:
			self.end_time = new_end_time
		if new_days:
			self.days = new_days
		if new_classroom:
			self.classroom = new_classroom
		if new_prereqs:
			self.prereqs = new_prereqs
		if new_coreqs:
			self.coreqs = new_coreqs
		if new_core:
			self.core = new_core

	def getSession(self):
		return self.session

	def addPrereq(self, new_prereq: str):
		self.prereqs.append(new_prereq)

	def addCoreq(self, new_coreq: str):
		self.coreqs.append(new_coreq)

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
				start_time = self.start_time,
				end_time = self.end_time,
				days = self.days,
				classroom = self.classroom,
				prereqs = self.prereqs,
				coreqs = self.coreqs,
				core = self.core
				)
		
		return Course(course_name = self.course_name, session = self.session, section = new_section, core = self.core)
