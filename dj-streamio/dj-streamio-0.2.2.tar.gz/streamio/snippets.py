from example_app.models import Todo
from datetime import datetime, date

actions = ['create', 'started', 'updated', 'done']
titles = [
    'do something',
    'do something else',
    'other stuff',
    'groceries',
    'have lunch',
]
for title in titles:
    Todo.objects.create(title=title)