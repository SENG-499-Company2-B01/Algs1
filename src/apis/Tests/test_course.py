from apis.models import Course
from unittest.mock import patch

# Create your tests here.

# Test1: Test for ChangeInfo
@patch(Course)
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

# Test3: Test for addPrereq

# Test4: Test for addCoreq

# Test5: Test for getOutputDict

# Test6: Test for cloneToSession

# Test7: Test for addSection
