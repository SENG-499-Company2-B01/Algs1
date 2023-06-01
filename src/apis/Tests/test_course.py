from apis.models import Course
from unittest.mock import patch

# Create your tests here.

def test_course_init():
	course = Course("SENG 275", 300, "FALL", "A01", "Prof", "9:00", "10:00", "MWF", "ECS 269", ["CSC 110"], ["SENG 250"], True)
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

# Test1: Test for ChangeInfo
@patch('apis.models.Course')
def test_changeInfo(TestCourse):
    # Mock Model class object
    
    TestCourse( 
        course_name="TEST101", 
        course_size=100, 
        session="Spring", 
        section="A01", 
        prof="Mr.Test", 
        start_time="OldStartTime", 
        end_time="OldEndTime", 
        days="M,R", 
        classroom="TESTROOM101", 
        prereqs=["PRE101"], 
        coreqs=["COREQ101"], 
        core=False)

    # Call model.changeInfo
    TestCourse.changeInfo(
        course_size=200, 
        session="Summer", 
        section="B01", 
        prof="Mrs.Test", 
        start_time="NewStartTime", 
        end_time="NewEndTime", 
        days="T,W,F", 
        classroom="TESTROOM202", 
        prereqs=["PRE202"], 
        coreqs=["COREQ202"], 
        core=True)
    # Assert
    assert TestCourse.course_size == 200
    assert TestCourse.session is "Summer"
    assert TestCourse.section is "B01"
    assert TestCourse.prof is "Mrs.Test"
    assert TestCourse.start_time is "NewStartTime"
    assert TestCourse.end_time is "NewEndTime"
    assert TestCourse.days is "T,W,F"
    assert TestCourse.classroom is "TESTROOM202"
    assert TestCourse.prereqs is ["PRE202"]
    assert TestCourse.coreqs is ["COREQ202"]
    assert TestCourse.core is True

# Test2: Test for getSession
def test_getSession():
	course = Course("SENG 275", 300, "FALL", "A01", "Prof", "9:00", "10:00", "MWF", "CAB 269", ["CSC 110"], ["SENG 250"], False)
	assert course.getSession() == "FALL"

# Test3: Test for addPrereq
def test_addPrereq():
	course = Course("SENG 275", 300, "FALL", "A01", "Prof", "9:00", "10:00", "MWF", "CAB 269", ["CSC 110"], ["SENG 250"], False)
	course.addPrereq("CSC 120")
	assert course.prereqs == ["CSC 110", "CSC 120"]

# Test4: Test for addCoreq

# Test5: Test for getOutputDict

# Test6: Test for cloneToSession

# Test7: Test for addSection
