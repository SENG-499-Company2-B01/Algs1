from apis.models import Course, TimeBlock
from unittest.mock import patch

# Create your tests here.

def test_course_init():
	course = Course( 
		course_name="SENG 275", 
	    course_size= 300, 
	    session="FALL", 
	    section="A01", 
	    prof="Prof", 
	    times= TimeBlock("A", M_start_time="9:00", M_end_time="10:00"), 
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
	#assert course.times.days["M"]["start"] == "9:00"
	#assert course.end_time == "10:00"
	#assert course.days == "MWF"
	assert course.classroom == "ECS 269"
	assert course.prereqs == ["CSC 110"]
	assert course.coreqs == ["SENG 250"]
	assert course.core == True

# Test1: Test for ChangeInfo
def test_changeInfo():
    course = Course(
		course_name="SENG 275", 
		course_size=300, session="FALL", 
		section="A01", prof="Prof", 
		times= TimeBlock("A", M_start_time="9:00", M_end_time="10:00"), 
		classroom="CAB 269", 
		prereqs=["CSC 110"], 
		coreqs=["SENG 250"], 
		core=False)
    course.changeInfo(course_size = 350, section = "A02", times = TimeBlock("A", M_start_time="9:00", M_end_time="11:00"), classroom = "ECS 269", prereqs = ["CSC 110", "CSC 120"], core = True)
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
	course = Course(
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
	course = Course(
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

# Test5: Test for getOutputDict

# Test6: Test for cloneToSession

# Test7: Test for addSection
