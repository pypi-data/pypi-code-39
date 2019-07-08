from intuginehelper.intudb import get_trips


query = '{"$and": [{"started_by": {"$in": ["mahindratest", "mahindraprod"]}}]}'

trips = get_trips(query,[1, 1, 2019], [1, 7, 2019])

print(len(trips))