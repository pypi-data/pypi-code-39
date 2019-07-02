from flask import Flask, Response
from pyrediseasyio import IOGroup, HMTLIOGroup, HTMLIO
from pyrediseasyio import StringIO, BooleanIO, FloatIO, IntIO
from dominate.tags import head, script, body, link, div, table
import dominate
import random


app = Flask(__name__)


class TestGroup(IOGroup):
    FirstName = StringIO("First Name", default="Steve")
    LastName = StringIO("Last Name", default="Jackson")
    Age = IntIO("Age", default=48, units="years")
    IsProgrammer = BooleanIO("Is a programmer", on_value="Yes", off_value="No", default=True)
    IsFather = BooleanIO("Is a father", on_value="Definately", off_value="Not yet", default=True)
    BathroomBreaks = IntIO("Bathroom breaks", default=3)

test_group = TestGroup()
html_test_group =HMTLIOGroup(test_group)


doc = dominate.document(title='Test Page')
with doc.head:
    link(rel='stylesheet', href='https://www.w3schools.com/w3css/4/w3.css')
    link(rel='stylesheet', href="/static/easyio.css")
    script(type='text/javascript', src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js')
    script(type='text/javascript', src='static/easyio.js')
with doc.body:
    with div(cls="flex-container"):
        with div(cls="w3-card w3-margin w3-border w3-padding"):
            html_test_group.html_table(
                headers=["ITEM", "VALUE", "UNITS"],
                show_units=True)
        with div(cls="w3-card w3-margin w3-border w3-padding"):
            html_test_group.html(
                headers=["ITEM", "VALUE", "UNITS"],
                show_set=False, show_reset=False, show_units=True, by_lambda_each=lambda x : 'Bathroom' not in x.addr)
    with table():
        HTMLIO(test_group.BathroomBreaks).html_row(show_reset=True, show_set=True, show_value=False)





@app.route('/')
def hello_world():
    html = doc.render()
    return Response(html)


@app.route('/api/io/getall')
def get_all_io():
    test_group.Age = random.randint(40,50)
    d = html_test_group.dumps()
    return Response(d)

@app.route('/api/io/<key>/<value>', methods=['POST'])
def set_io(key: str, value: str):
    test_group.write(key, value)




if __name__ == '__main__':
   app.run(debug=True)