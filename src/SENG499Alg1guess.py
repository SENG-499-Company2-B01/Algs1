class course:
    self.course_number="SENG499"
    self.course_CRN=30037
    self.course_student_size=72
    self.course_happening_numbers=1
    self.course_length=180
    self.course_proferror_requirement=[]
    self.course_classroom_requirement=[]
    self.assigned_classroom=-1
    self.assigned_professor=-1
    self.assigned_timezone=-1
    self.clpir=-1
    self.pfpir=-1
    def __init__(self,coursenumber,CRN,student_size,happening_numbers,length,proferror_requirement,classroom_requirement):
        self.course_number=coursenumber
        self.course_CRN=CRN
        self.course_student_size=student_size
        self.course_happening_numbers=happening_numbers
        self.course_length=length
        self.course_proferror_requirement=[]
        self.course_classroom_requirement=[]
        for e in proferror_requirement:
            self.course_proferror_requirement.append(e)
        for e in classroom_requirement:
            self.course_classroom_requirement.append(e)
class professor:
    self.professor_stream =0
    self.class_preference=[]
    self.employee_id=0
    self.employee_name="Chi Zhang"
    self.perfered_timetable=[]#Professor’s time preference the time preference is specified by a string of letter with each letter repersenting a time span within the uvic time table
	self.unavailable_timetable=[]
    self.qualification=[]
    self.assigned_schedule=[]
    def __init__(self,stream,class_crn_prefered,personal_id,name,ptimetable,utimetable,qualification):
        self.professor_stream =stream
        self.class_preference=[]
        for e in class_crn_prefered:
            self.class_preference.append(e)
        self.employee_id=personal_id
        self.employee_name=name
        self.perfered_timetable=[]
        self.unavailable_timetable=[]
        self.qualification=[]
        for e in ptimetable:
            self.perfered_timetable.append(e)
        for e in utimetable:
            self.unavailable_timetable.append(e)
        for e in qualification:
            self.qualification.append(e)
class classroom:
    self.address ="EWS124"
    self.size=2048
    self.equipment=[]
    self.department="ENG"
    self.assigned_zone=[]
    def __init__(self,add,siz,equ,dpt):
        self.address =add
        self.size=siz
        self.equipment=[]
        for e in qualification:
            self.equipment.append(e)
        self.department=dpt
class resultingschedule:
    self.course ="SENG499"
    self.professorid="abce"
    self.address="ELW127"
    self.timezone="A"
    self.semester="F"
    def __init__(self,cs,pf,ad,tm,sm):
        self.course =cs
        self.professorid=pf
        self.address=ad
        self.timezone=tm
        self.semester=sm
def int pfqualitycheck(pf,course):
    for r in course.course_proferror_requirement:
        if r not in pf.qualification:
            return 0
    return 1
def int crqualitycheck(cl,course):
    for r in course.course_classroom_requirement:
        if r not in cl.equipment:
            return 0
    return 1
classroomlist=[]
professorlist=[]
courselist=[]
def int class_rank_priority(course):
    k=0
    for n in classroomlist:
        if(crqualitycheck(n,course)):
            k=k+1
    return k
def int prof_rank_priority(course):
    k=0
    for n in professorlist:
        if(pfqualitycheck(n,course)):
            k=k+1
    return k
Ntime_schedule=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U"]
def int assign(course,prof):
    for k in Ntime_schedule:
        if (k,"F") not in prof.assigned_schedule && len(prof.assigned_schedule)<3:
            for m in classroomlist:
                if(crqualitycheck(m,course)==1 && (k,"F") not in m.assigned_zone):
                        m.assigned_zone.append((k,"F"))
                        prof.assigned_schedule.append((k,"F"))
                        course.assigned_classroom=m.address
                        course.assigned_professor=prof.id
                        course.assigned_timezone=(k,"F")
                        return 1
    for k in Ntime_schedule:
        if (k,"Su") not in prof.assigned_schedule && len(prof.assigned_schedule)<3:
            for m in classroomlist:
                if(crqualitycheck(m,course)==1 && (k,"Su") not in m.assigned_zone):
                        m.assigned_zone.append((k,"Su"))
                        prof.assigned_schedule.append((k,"Su"))
                        course.assigned_classroom=m.address
                        course.assigned_professor=prof.id
                        course.assigned_timezone=(k,"Su")
                        return 1
    for k in Ntime_schedule:
        if (k,"Sp") not in prof.assigned_schedule && len(prof.assigned_schedule)<3:
            for m in classroomlist:
                if(crqualitycheck(m,course)==1 && (k,"Sp") not in m.assigned_zone):
                        m.assigned_zone.append((k,"Sp"))
                        prof.assigned_schedule.append((k,"Sp"))
                        course.assigned_classroom=m.address
                        course.assigned_professor=prof.id
                        course.assigned_timezone=(k,"Sp")
                        return 1
    return 0
def random_addsign(courselist):
    sem=0
    courselist.sort(key=prof_rank_priority)
    for n in courselist:
        for k in professorlist:
            if(pfqualitycheck(k,n)):
                if(assign(n,k)==1):
                    return 1
                else:
                    continue