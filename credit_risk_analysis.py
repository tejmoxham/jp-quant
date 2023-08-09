
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import pandas as pd

# Train classifier using raw data
df = pd.read_csv('./data/loan_data.csv')
features = ['credit_lines_outstanding', 'debt_to_income', 'payment_to_income', 'years_employed', 'fico_score']
df['payment_to_income'] = df['loan_amt_outstanding'] / df['income']
df['debt_to_income'] = df['total_debt_outstanding'] / df['income']
clf = LogisticRegression(random_state=0, solver='liblinear', tol=1e-5, max_iter=10000).fit(df[features].values, df['default'])

# Define expected loss model
def expected_loss(df):
    df['payment_to_income'] = df['loan_amt_outstanding'] / df['income']
    df['debt_to_income'] = df['total_debt_outstanding'] / df['income']
    default_prob = clf.predict_proba(df[features].values.reshape(1, -1))
    return  default_prob[0,1]*df['loan_amt_outstanding']*0.1  
