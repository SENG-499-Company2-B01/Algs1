from cat_swarm import main
import json
from datetime import datetime
import numpy as np

def time_in_range(start, end, x):
    #Return true if x is in the range [start, end]
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
    
with open('testing_subset.json') as f:
    data = f.read()
    input_sched = json.loads(data)
# with open('time_blocks.json') as f:
#     data = f.read()
#     input_timeblocks = json.loads(data)
    
input_user = input_sched['users']
input_courses = input_sched['courses']
input_classrooms = input_sched['classrooms']

print(len(input_user))
print(len(input_courses))
print(len(input_classrooms))
# # for prof in input_user:
# #     timeblock_pref_dict = {}
# #     for time_list_outer in prof['time_pref'].keys():
# #         for time_list_count in range(len(prof['time_pref'][time_list_outer])):
            
                
# #             start_time = datetime.strptime(prof['time_pref'][time_list_outer][time_list_count][0], '%H:%M')
# #             end_time = datetime.strptime(prof['time_pref'][time_list_outer][time_list_count][1], '%H:%M')
            
# #             for time_letter in input_timeblocks.keys():
# #                 add_time_flag = 0
# #                 for day in input_timeblocks[time_letter].keys():
# #                     class_start = datetime.strptime(input_timeblocks[time_letter][day]["start"], '%H:%M')
# #                     class_end = datetime.strptime(input_timeblocks[time_letter][day]["end"], '%H:%M')
# #                     if time_in_range(start_time,end_time,class_start) and time_in_range(start_time,end_time,class_end):
# #                         add_time_flag = 1
# #                     else:
# #                         add_time_flag = 0
# #                         break
# #                 if add_time_flag == 1:
# #                     timeblock_pref_dict[time_letter] = input_timeblocks[time_letter]
        
# #     prof['timeblocks'] = timeblock_pref_dict


scheduled_courses = main(input_user, input_courses, input_classrooms)

print(scheduled_courses)

#print(np.random.uniform(-5,5,20).tolist())
#print(min([5,4,3,9,1,0,4,8], 0.2*9))