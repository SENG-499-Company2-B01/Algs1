from django.test import TestCase
from .. import models
import pytest



# Create your tests here.

# Test1: Test for ChangeInfo
def test_course_init():
	course = models.Course("SENG 275", 300, "FALL", "A01", "Prof", "9:00", "10:00", "MWF", "ECS 269", ["CSC 110"], ["SENG 250"], True)
	assert course.course_name == "SENG 275"
	assert course.course_size == 300
	assert course.session == "FALL"
	assert course.section == "A01"
	assert course.prof == "Prof"
	assert course.start_time == "9:00"
	assert course.end_time == "10:00"
	assert course.days == "MWF"
	assert course.classroom == "ECS 269"
	assert course.prereqs == ["CSC 110"]
	assert course.coreqs == ["SENG 250"]
	assert course.core == True

def test_change_courseInfo():
	course = models.Course("SENG 275", 300, "FALL", "A01", "Prof", "9:00", "10:00", "MWF", "CAB 269", ["CSC 110"], ["SENG 250"], False)
	course.changeInfo(new_course_size = 300, new_section = "A02", new_end_time = "11:00", new_classroom = "ECS 269", new_prereqs = ["CSC 110", "CSC 120"], new_core = True)
	assert course.course_name == "SENG 275"
	assert course.course_size == 300
	assert course.session == "FALL"
	assert course.section == "A02"
	assert course.prof == "Prof"
	assert course.start_time == "9:00"
	assert course.end_time == "11:00"
	assert course.days == "MWF"
	assert course.classroom == "ECS 269"
	assert course.prereqs == ["CSC 110", "CSC 120"]
	assert course.coreqs == ["SENG 250"]
	assert course.core == True
# Test2: Test for getSession

def test_getSession():
	course = models.Course("SENG 275", 300, "FALL", "A01", "Prof", "9:00", "10:00", "MWF", "CAB 269", ["CSC 110"], ["SENG 250"], False)
	assert course.getSession() == "FALL"

# Test3: Test for addPrereq
def test_addPrereq():
	course = models.Course("SENG 275", 300, "FALL", "A01", "Prof", "9:00", "10:00", "MWF", "CAB 269", ["CSC 110"], ["SENG 250"], False)
	course.addPrereq("CSC 120")
	assert course.prereqs == ["CSC 110", "CSC 120"]
# Test4: Test for addCoreq

# Test5: Test for getOutputDict

# Test6: Test for cloneToSession

# Test7: Test for addSection
