from flask import (
    request, Blueprint, render_template, flash, redirect, url_for
)
from gorillaml.lab import authorize
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, validators, ValidationError

gorillaml = Blueprint('simple_dashboard', __name__, url_prefix='/simple_dashboard', template_folder='templates', static_folder='static')

class SimpleDashboardForm(FlaskForm):
    string_field = StringField('StringField', [validators.DataRequired()])
    select_field = SelectField('SelectField', choices=[('enabled', 'Enable'), ('disabled', 'Disable')])
    textarea_field = TextAreaField('TextAreaField', [validators.DataRequired()])
    boolean_field = BooleanField('BooleanField')

@gorillaml.route('/', methods=['GET', 'POST'])
@authorize
def index():
    form = SimpleDashboardForm()
    if form.validate_on_submit():
        flash('Your success message','success')
        flash('Your error message','error')

        return redirect(url_for('simple_dashboard.index'))
    
    return render_template('simple_dashboard.html', form=form)