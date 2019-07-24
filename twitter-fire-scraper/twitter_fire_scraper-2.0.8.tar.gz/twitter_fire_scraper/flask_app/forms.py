from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class ScrapeSingleTermTestForm(FlaskForm):
    term = StringField('term', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[NumberRange(1, 1000)])