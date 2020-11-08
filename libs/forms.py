from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class EntryForm(FlaskForm):
    deal_name = StringField('DealName', validators=[DataRequired])
    deal_price = IntegerField('Price', valdidators=[DataRequired])
