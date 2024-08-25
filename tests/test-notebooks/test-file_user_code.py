import pandas as pd
import numpy as np
import statsmodels
import statsmodels.api as sm
import sqlite3
import plotly.express as px
import unittest

tc = unittest.TestCase()

a = 1
b = 2

# YOUR CODE BEGINS
c = a + b
# YOUR CODE ENDS

nsample = 100
x = np.linspace(0, 10, 100)
X = np.column_stack((x, x ** 2))
beta = np.array([1, 0.1, 10])
e = np.random.normal(size=nsample)

X = sm.add_constant(X)
y = np.dot(X, beta) + e

# YOUR CODE BEGINS
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())
# YOUR CODE ENDS

# YOUR CODE BEGINS
df_marketing = pd.read_csv("https://github.com/UI-Deloitte-business-analytics-center/datasets/blob/main/bank-direct-marketing.csv?raw=true")
df_marketing = df_marketing[["age", "job", "place_deposit"]]
df_marketing.head()
# YOUR CODE ENDS

df_test = pd.read_csv("https://github.com/UI-Deloitte-business-analytics-center/datasets/blob/main/bank-direct-marketing.csv?raw=true")
df_test

df_marketing = pd.read_csv("https://github.com/UI-Deloitte-business-analytics-center/datasets/blob/main/bank-direct-marketing.csv?raw=true")

# create a blank SQLite db file
conn = sqlite3.connect('marketing.db')

c = conn.cursor()

# Drop (delete) listings table if it already exists
c.execute('DROP TABLE IF EXISTS campaigns')
conn.commit()

create_table_query = '''
CREATE TABLE IF NOT EXISTS campaigns (
    age INT,
    job TEXT,
    marital TEXT,
    education TEXT,
    contact_type TEXT,
    num_contacts INT,
    prev_outcome TEXT,
    place_deposit INT
)
'''

c.execute(create_table_query)
conn.commit()

tables = list(pd.read_sql_query('SELECT * FROM sqlite_master WHERE type="table";', con=conn)['tbl_name'])
if 'campaigns' in tables:
    c.execute(f'DELETE FROM campaigns')
    conn.commit()
    
df_marketing.to_sql(name='campaigns', index=False, con=conn, if_exists='append')

conn.close()

d = 10.5
e = 2

# YOUR CODE BEGINS
f = d // e
# YOUR CODE ENDS

f

df_gold = pd.read_csv('https://github.com/bdi475/datasets/raw/main/gold-annual-closing-price.csv')

fig = px.line(df_gold, x='Year', y='Closing Price', title='Annual Closing Price of Gold')
fig.show()

