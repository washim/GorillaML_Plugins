"""
GorillaML is created based on Flask framework and this plugins created
based on Flask blueprint framework. You have full controll to play with
this plugins using Flask blueprint.
For more details start reading https://flask.palletsprojects.com/en/1.1.x/blueprints/
"""

from flask import (
    request, Blueprint, render_template, flash, redirect, url_for, current_app
)
from gorillaml.lab import authorize, plugin_path, fig_to_html
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SelectField, SelectMultipleField, validators

import os
from matplotlib import pyplot
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

# This is manadatory to create gorillaml plugins. Dont change this variable name else plugin will not work
gorillaml = Blueprint('cross_validation_score_regression', __name__, url_prefix='/cross_validation_score_regression', 
                      template_folder='templates', static_folder='static')

class RegressionCrossValidationForm(FlaskForm):
    """
    For more details start reading https://flask-wtf.readthedocs.io/en/stable/
    """
    algo_choices = [
        ('LinearRegression', 'LinearRegression'), 
        ('LASSO', 'LASSO'), ('ElasticNet','ElasticNet'), ('KNeighborsRegressor','KNeighborsRegressor'), 
        ('DecisionTreeRegressor','DecisionTreeRegressor'), ('SupportVectorRegressor','SupportVectorRegressor')
    ]
    regression_scoring_choices = [
        ('explained_variance','explained_variance'), ('max_error','max_error'), ('neg_mean_absolute_error','neg_mean_absolute_error'), 
        ('neg_mean_squared_error','neg_mean_squared_error'), ('neg_median_absolute_error','neg_median_absolute_error')
    ]
    split_size = FloatField('Test validation size', [validators.DataRequired()])
    kfold = IntegerField('K Fold split size', [validators.DataRequired()])
    algo = SelectMultipleField('Choose model to compare', [validators.DataRequired()], choices=algo_choices)
    regression_scoring = SelectField('Regression Scoring Parameter', [validators.DataRequired()], choices=regression_scoring_choices)

@gorillaml.route('/', methods=['GET', 'POST'])
@authorize
def index():
    """
    If you want url to view by any one then @authorize wont be necessary
    """
    models_data = []
    plot_html = ''
    form = RegressionCrossValidationForm()
    if form.validate_on_submit():
        filename = os.path.join(plugin_path('cross_validation_score_regression', 'admin'), 'housing.csv')
        names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
        dataset = read_csv(filename, delim_whitespace=True, names=names)
        array = dataset.values
        X = array[:,0:13]
        Y = array[:,13]
        validation_size = form.split_size.data
        X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size, random_state=1)
        models = []
        for model in form.algo.data:
            if model == 'LinearRegression':
                models.append((model, LinearRegression()))
            elif model == 'LASSO':
                models.append((model, Lasso()))
            elif model == 'ElasticNet':
                models.append((model, ElasticNet()))
            elif model == 'KNeighborsRegressor':
                models.append((model, KNeighborsRegressor()))
            elif model == 'DecisionTreeRegressor':
                models.append((model, DecisionTreeRegressor()))
            elif model == 'SupportVectorRegressor':
                models.append((model, SVR()))
        results = []
        names = []
        for name, model in models:
            kfold = KFold(n_splits=form.kfold.data, random_state=1)
            cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=form.regression_scoring.data)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            models_data.append(msg)
        
        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        pyplot.boxplot(results)
        pyplot.xticks(rotation='vertical')
        ax.set_xticklabels(names)
        pyplot.subplots_adjust(bottom=0.35)
        plot_html = fig_to_html(fig)
    
    return render_template('index.html', form=form, models_data=models_data, plot_html=plot_html)
