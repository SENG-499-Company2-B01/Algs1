from scheduler import cat_swarm
def test_cso():
    with open('/testing_subset.json') as f:
        data = f.read()
        input_data=json.loads(data)
    input_profs=input_data["users"]
    input_courses=input_data["courses"]
    input_classrooms=input_data["classrooms"]
    with open('/app/time_blocks.json') as f:
        data = f.read()
        input_timeblocks = json.loads(data)
    population_size=
    best_solution = cat_swarm_optimization(input_profs, input_courses, input_classrooms, input_timeblocks, len(input_profs), 1000)
    assert best_solution['fitness'] >=0
    return 0