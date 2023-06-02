from .. import models
from unittest.mock import patch

# Create your tests here.

def test_course_init():
	course = models.Course( 
		course_name="SENG 275", 
	    course_size= 300, 
	    session="FALL", 
	    section="A01", 
	    prof="Prof", 
	    times= models.TimeBlock("A", M_start_time="9:00", M_end_time="10:00"), 
        classroom="ECS 269", 
	    prereqs=["CSC 110"], 
	    coreqs=["SENG 250"], 
	    core=True)
	print(course.course_name)
	assert course.course_name == "SENG 275"
	assert course.course_size == 300
	assert course.session == "FALL"
	assert course.section == "A01"
	assert course.prof == "Prof"
	#assert course.start_time == "9:00"
	assert course.times.days["M"]["start"] == "9:00"
	#assert course.end_time == "10:00"
	#assert course.days == "MWF"
	assert course.classroom == "ECS 269"
	assert course.prereqs == ["CSC 110"]
	assert course.coreqs == ["SENG 250"]
	assert course.core == True

# Test1: Test for ChangeInfo
def test_changeInfo():
    course = models.Course(
		course_name="SENG 275", 
		course_size=300, session="FALL", 
		section="A01", prof="Prof", 
		times= models.TimeBlock("A", M_start_time="9:00", M_end_time="10:00"), 
		classroom="CAB 269", 
		prereqs=["CSC 110"], 
		coreqs=["SENG 250"], 
		core=False)
    course.changeInfo(course_size = 350, section = "A02", times = models.TimeBlock("A", M_start_time="9:00", M_end_time="11:00"), classroom = "ECS 269", prereqs = ["CSC 110", "CSC 120"], core = True)
    assert course.course_name == "SENG 275"
    assert course.course_size == 350
    assert course.session == "FALL"
    assert course.section == "A02"
    assert course.prof == "Prof"
	#assert course.start_time == "9:00"
	#assert course.end_time == "11:00"
    assert course.times.days["M"]["end"] == "11:00"
	#assert course.days == "MWF"
    assert course.classroom == "ECS 269"
    assert course.prereqs == ["CSC 110", "CSC 120"]
    assert course.coreqs == ["SENG 250"]
    assert course.core == True

# Test2: Test for getSession
def test_getSession():
	course = models.Course(
		course_name="SENG 275", 
	    course_size=300, 
	    session="FALL", 
	    section="A01",
	    prof= "Prof", 
	    classroom="CAB 269", 
	    prereqs=["CSC 110"], 
	    coreqs=["SENG 250"], 
	    core=False)
	assert course.getSession() == "FALL"

# Test3: Test for addPrereq
def test_addPrereq():
	course = models.Course(
		course_name="SENG 275", 
	    course_size=300, 
	    session="FALL", 
	    section="A01",
	    prof= "Prof", 
	    classroom="CAB 269", 
	    prereqs=["CSC 110"], 
	    coreqs=["SENG 250"], 
	    core=False)
	course.addPrereq("CSC 120")
	assert course.prereqs == ["CSC 110", "CSC 120"]

# Test4: Test for addCoreq
def test_addCoreq():
	course = models.Course(
		course_name="SENG 275", 
	    course_size=300, 
	    session="FALL", 
	    section="A01",
	    prof= "Prof", 
	    classroom="CAB 269", 
	    prereqs=["CSC 110"], 
	    coreqs=["SENG 250"], 
	    core=False)
	course.addCoreq("CSC 120")
	assert course.coreqs == ["SENG 250", "CSC 120"]

# Test5: Test for getOutputDict
def test_getOutputDict():
	course = models.Course(
		course_name="SENG 275", 
	    course_size=300, 
	    session="FALL", 
	    section="A01",
	    prof= "Prof",
	    times= models.TimeBlock("A", M_start_time="9:00", M_end_time="10:00"), 
	    classroom="CAB 269", 
	    prereqs=["CSC 110"], 
	    coreqs=["SENG 250"], 
	    core=False)
	result = course.getOutputDict()
	assert course.times is not None
	assert result == {
		'Course': "SENG 275",
		'Section': "A01",
		'Prof': "Prof",
		'Times': {"M": {"start": "9:00", "end": "10:00"}},
		'Class': "CAB 269",
		'Course Size': 300
    }

# Test6: Test for cloneToSession
def test_cloneToSession():
	courseToClone = models.Course(
		course_name="SENG 275", 
	    course_size=300, 
	    session="FALL", 
	    section="A01",
	    prof= "Prof",
	    times= models.TimeBlock("A", M_start_time="9:00", M_end_time="10:00"), 
	    classroom="CAB 269", 
	    prereqs=["CSC 110"], 
	    coreqs=["SENG 250"], 
	    core=False)
	clonedCourse = courseToClone.cloneToSession("SPRING")
	assert clonedCourse.course_name == "SENG 275"
	assert clonedCourse.course_size == 300
	assert clonedCourse.prof == "Prof"
	assert clonedCourse.times == courseToClone.times
	assert clonedCourse.classroom == "CAB 269"
	assert clonedCourse.prereqs == ["CSC 110"]
	assert clonedCourse.coreqs == ["SENG 250"]
	assert clonedCourse.core == False
	assert clonedCourse.session == "SPRING"

# Test7: Test for addSection
def test_addSection():
	course = models.Course(
		course_name="SENG 275", 
	    course_size=300, 
	    session="FALL", 
	    section="A01",
	    prof= "Prof",
	    times= models.TimeBlock("A", M_start_time="9:00", M_end_time="10:00"), 
	    classroom="CAB 269", 
	    prereqs=["CSC 110"], 
	    coreqs=["SENG 250"], 
	    core=False)
	result1 = course.addSection(new_section="B01", same_info=True)
	assert result1.course_name == course.course_name
	assert result1.section == "B01"
	result2 = course.addSection(new_section=False)
	assert result2.course_name == "SENG 275"
	assert result2.section == "A02"
	 