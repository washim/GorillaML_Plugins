"""
GorillaML is created based on Flask framework and this plugins created
based on Flask blueprint framework. You have full controll to play with
this plugins using Flask blueprint.
For more details start reading https://flask.palletsprojects.com/en/1.1.x/blueprints/
"""

from flask import (
    Blueprint, render_template
)
from gorillaml.lab import authorize, plugin_path, fig_to_html
from .form import RegressionCrossValidationForm, ClassificationCrossValidationForm

import os
from matplotlib import pyplot
from pandas import read_csv
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Lasso, ElasticNet, LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVR, SVC

# This is manadatory to create gorillaml plugins. Dont change this variable name else plugin will not work
gorillaml = Blueprint('cross_validation_score', __name__, url_prefix='/cross_validation_score',
                      template_folder='templates', static_folder='static')

@gorillaml.route('/', methods=['GET', 'POST'])
@authorize
def index():
    return render_template('index.html')


@gorillaml.route('/regression', methods=['GET', 'POST'])
@authorize
def regression():
    """
    If you want url to view by any one then @authorize wont be necessary
    """
    models_data = []
    plot_html = ''
    form = RegressionCrossValidationForm()
    if form.validate_on_submit():
        filename = os.path.join(plugin_path('cross_validation_score', 'admin'), 'housing.csv')
        names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
        dataset = read_csv(filename, delim_whitespace=True, names=names)
        array = dataset.values
        X = array[:,0:13]
        Y = array[:,13]
        models = []
        for model in form.algo.data:
            if model == 'LR':
                models.append((model, LinearRegression()))
            elif model == 'LASSO':
                models.append((model, Lasso()))
            elif model == 'EN':
                models.append((model, ElasticNet()))
            elif model == 'KNN':
                models.append((model, KNeighborsRegressor()))
            elif model == 'DTR':
                models.append((model, DecisionTreeRegressor()))
            elif model == 'SVR':
                models.append((model, SVR()))
        results = []
        names = []
        for name, model in models:
            kfold = KFold(n_splits=form.kfold.data, random_state=1)
            cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=form.scoring.data)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            models_data.append(msg)
        
        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        pyplot.boxplot(results)
        pyplot.xticks(rotation=60)
        pyplot.tight_layout()
        pyplot.subplots_adjust(bottom=0.2)
        ax.set_xticklabels(names)
        plot_html = fig_to_html(fig)
    
    return render_template('regression.html', form=form, models_data=models_data, plot_html=plot_html)


@gorillaml.route('/classification', methods=['GET', 'POST'])
@authorize
def classification():
    """
    If you want url to view by any one then @authorize wont be necessary
    """
    models_data = []
    plot_html = ''
    form = ClassificationCrossValidationForm()
    if form.validate_on_submit():
        filename = os.path.join(plugin_path('cross_validation_score', 'admin'), 'pima-indians-diabetes.data.csv')
        names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
        dataset = read_csv(filename, names=names)
        array = dataset.values
        X = array[:, 0:8]
        Y = array[:, 8]
        models = []
        for model in form.algo.data:
            if model == 'LR':
                models.append((model, LogisticRegression()))
            elif model == 'LDA':
                models.append((model, LinearDiscriminantAnalysis()))
            elif model == 'KNN':
                models.append((model, KNeighborsClassifier()))
            elif model == 'CART':
                models.append((model, DecisionTreeClassifier()))
            elif model == 'NB':
                models.append((model, GaussianNB()))
            elif model == 'SVM':
                models.append((model, SVC()))
        results = []
        names = []
        for name, model in models:
            kfold = KFold(n_splits=form.kfold.data, random_state=7)
            cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=form.scoring.data)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            models_data.append(msg)

        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        pyplot.boxplot(results)
        pyplot.xticks(rotation=60)
        pyplot.tight_layout()
        pyplot.subplots_adjust(bottom=0.2)
        ax.set_xticklabels(names)
        plot_html = fig_to_html(fig)

    return render_template('classification.html', form=form, models_data=models_data, plot_html=plot_html)
