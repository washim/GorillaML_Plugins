from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SelectMultipleField, SubmitField, validators


class RegressionCrossValidationForm(FlaskForm):
    """
    For more details start reading https://flask-wtf.readthedocs.io/en/stable/
    """
    algo_choices = [
        ('LR', 'LinearRegression'),
        ('LASSO', 'LASSO'), ('EN','ElasticNet'), ('KNN','KNeighborsRegressor'),
        ('DTR','DecisionTreeRegressor'), ('SVR','SupportVectorRegressor')
    ]
    scoring_choices = [
        ('explained_variance','explained_variance'), ('max_error','max_error'), ('neg_mean_absolute_error','neg_mean_absolute_error'),
        ('neg_mean_squared_error','neg_mean_squared_error'), ('neg_median_absolute_error','neg_median_absolute_error'), ('r2','r2')
    ]
    kfold = IntegerField('K Fold split size', [validators.DataRequired()], default=7)
    algo = SelectMultipleField('Choose model to compare', [validators.DataRequired()], choices=algo_choices, default=['LR','LASSO','EN','KNN','DTR','SVR'])
    scoring = SelectField('Regression Scoring Parameter', [validators.DataRequired()], choices=scoring_choices, default='r2')
    submit = SubmitField('Compare')

class ClassificationCrossValidationForm(FlaskForm):
    algo_choices = [
        ('LR', 'LogisticRegression'),
        ('LDA', 'LinearDiscriminantAnalysis'), ('KNN', 'KNeighborsClassifier'),
        ('CART', 'DecisionTreeClassifier'), ('NB', 'GaussianNB'), ('SVM', 'SVC')
    ]
    scoring_choices = [
        ('accuracy', 'accuracy'), ('balanced_accuracy', 'balanced_accuracy'),
        ('average_precision', 'average_precision'),
        ('brier_score_loss', 'brier_score_loss'),
        ('f1', 'f1'), ('f1_micro', 'f1_micro'), ('f1_macro', 'f1_macro'), ('f1_weighted', 'f1_weighted'), ('f1_samples', 'f1_samples'),
        ('neg_log_loss', 'neg_log_loss'), ('precision', 'precision'), ('recall', 'recall'), ('jaccard', 'jaccard'), ('roc_auc', 'roc_auc')
    ]
    kfold = IntegerField('K Fold split size', [validators.DataRequired()], default=10)
    algo = SelectMultipleField('Choose model to compare', [validators.DataRequired()], choices=algo_choices, default=['LR', 'LDA', 'KNN', 'CART', 'NB', 'SVM'])
    scoring = SelectField('Regression Scoring Parameter', [validators.DataRequired()], choices=scoring_choices, default='roc_auc')
    submit = SubmitField('Compare')