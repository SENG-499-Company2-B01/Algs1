from openpyxl import load_workbook
import json, random

wb = load_workbook('Course_Summary_2022_2023.xlsx')
ws = wb.active

courses = { "courses": []}
for index, row in enumerate(ws.iter_rows(values_only=True)):
    if index > 0:
        try:
            if (row[2] == "CSC" or row[2] == "SENG") and row[4] == "A01":
                courses["courses"].append(
                    {
                        "course": f'{row[2]} {row[3]}',
                        "term": {
                            "winter": bool(random.getrandbits(1)),
                            "spring": bool(random.getrandbits(1)),
                            "summer": bool(random.getrandbits(1))
                        },
                        "enrollment": f'{row[18]}',
                        "prereqs": [],
                        "coreqs": []
                    }
                )
        except:
            print(row)
jsonObject = json.dumps(courses, indent=4)
with open("mockdata.json", "w") as outfile:
    outfile.write(jsonObject)