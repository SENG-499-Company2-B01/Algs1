from django.test import TestCase
from apis import models
import pytest



# Create your tests here.

# Test1: Test for ChangeInfo


def test_change_courseInfo():
	course = models.Course("SENG 275", 300, "FALL", "A01", "Prof", "9:00", "10:00", "MWF", "CAB 269", ["CSC 110"], ["SENG 250"], False)
	course.changeInfo(new_course_size = 350, new_section = "A02", new_end_time = "11:00", new_classroom = "ECS 269", new_prereqs = ["CSC 110", "CSC 120"], new_core = True)
	assert course.course_name == "SENG 275"
	assert course.course_size == 350
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


# Test4: Test for addCoreq

# Test5: Test for getOutputDict

# Test6: Test for cloneToSession

# Test7: Test for addSection
