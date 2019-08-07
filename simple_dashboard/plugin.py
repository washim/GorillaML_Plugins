"""
GorillaML is created based on Flask framework and this plugins created
based on Flask blueprint framework. You have full controll to play with
this plugins using Flask blueprint.
For more details start reading https://flask.palletsprojects.com/en/1.1.x/blueprints/
"""

from flask import (
    Blueprint, render_template, flash, redirect, url_for
)
from gorillaml.lab import authorize
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, validators

# This is manadatory to create gorillaml plugins. Dont change this variable name else plugin will not work
gorillaml = Blueprint('simple_dashboard', __name__, url_prefix='/simple_dashboard', 
                      template_folder='templates', static_folder='static')

class SimpleDashboardForm(FlaskForm):
    """
    For more details start reading https://flask-wtf.readthedocs.io/en/stable/
    """
    string_field = StringField('StringField', [validators.DataRequired()])
    select_field = SelectField('SelectField', choices=[('enabled', 'Enable'), ('disabled', 'Disable')])
    textarea_field = TextAreaField('TextAreaField', [validators.DataRequired()])
    boolean_field = BooleanField('BooleanField')

@gorillaml.route('/', methods=['GET', 'POST'])
@authorize
def index():
    """
    If you want url to view by any one then @authorize wont be necessary
    """
    form = SimpleDashboardForm()
    if form.validate_on_submit():
        flash('Your success message','success')
        flash('Your error message','error')

        return redirect(url_for('simple_dashboard.index'))
    
    return render_template('index.html', form=form)
