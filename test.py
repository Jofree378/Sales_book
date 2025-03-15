import json

with open('fixture/tests_data.json') as f:
    data = json.load(f)

for el in data:
    print(el['model'])    

