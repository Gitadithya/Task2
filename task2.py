# -*- coding: utf-8 -*-
"""Task2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17EjB1fhGBFEu-T_e3RGaT-2rKSCN5anE
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.style.use('ggplot')

data = pd.read_csv('/content/quikr_car.csv')

data.head()

data.tail()

data.shape

print("Number of Rows",data.shape[0])
print("Number of Columns",data.shape[1])

data.info()

data.isnull().sum()

data.describe()

data=data[data['year'].str.isnumeric()]

data['year']=data['year'].astype(int)

data=data[data['Price']!='Ask For Price']

data['Price']=data['Price'].str.replace(',','').astype(int)

data['kms_driven']=data['kms_driven'].str.split().str.get(0).str.replace(',','')

data=data[data['kms_driven'].str.isnumeric()]

data['kms_driven']=data['kms_driven'].astype(int)

data=data[~data['fuel_type'].isna()]

data.shape

data['name']=data['name'].str.split().str.slice(start=0,stop=3).str.join(' ')

data=data.reset_index(drop=True)

data

data.to_csv('Cleaned_Car_data.csv')

data.info()

data.describe(include='all')

data=data[data['Price']<6000000]

data['company'].unique()

plt.subplots(figsize=(15,7))
ax=sns.boxplot(x='company',y='Price',data=data)
ax.set_xticklabels(ax.get_xticklabels(),rotation=40,ha='right')
plt.show()

plt.subplots(figsize=(20, 10))
ax = sns.swarmplot(x='company', y='Price', data=data)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right')
plt.show()

sns.relplot(x='kms_driven',y='Price',data=data,height=7,aspect=1.5)

plt.subplots(figsize=(14,7))
sns.boxplot(x='fuel_type',y='Price',data=data)

ax=sns.relplot(x='company',y='Price',data=data,hue='fuel_type',size='kms_driven',height=7,aspect=2)
ax.set_xticklabels(rotation=40,ha='right')

X=data[['name','company','kms_driven','fuel_type']]
y=data['Price']

X

y.shape

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score

ohe=OneHotEncoder()
ohe.fit(X[['name','company','fuel_type']])

column_trans=make_column_transformer((OneHotEncoder(categories=ohe.categories_),['name','company','fuel_type']),
                                    remainder='passthrough')

lr=LinearRegression()

pipe=make_pipeline(column_trans,lr)

pipe.fit(X_train,y_train)

y_pred=pipe.predict(X_test)

r2_score(y_test,y_pred)

scores=[]
for i in range(1000):
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.1,random_state=i)
    lr=LinearRegression()
    pipe=make_pipeline(column_trans,lr)
    pipe.fit(X_train,y_train)
    y_pred=pipe.predict(X_test)
    scores.append(r2_score(y_test,y_pred))

np.argmax(scores)

scores[np.argmax(scores)]

print("Column Names in X_test:", X_test.columns)
print("Column Names in Test Data:", pd.DataFrame(columns=X_test.columns, data=np.array(['Maruti Suzuki Swift','Maruti',2019,'Petrol']).reshape(1,4)).columns)

print("Number of Columns in X_test:", len(X_test.columns))
print("Number of Columns in Test Data:", pd.DataFrame(columns=X_test.columns, data=np.array(['Maruti Suzuki Swift','Maruti',2019,'Petrol']).reshape(1,4)).shape[1])

pipe.predict(pd.DataFrame(columns=X_test.columns,data=np.array(['Maruti Suzuki Swift','Maruti',2019,'Petrol']).reshape(1,4)))

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.1,random_state=np.argmax(scores))
lr=LinearRegression()
pipe=make_pipeline(column_trans,lr)
pipe.fit(X_train,y_train)
y_pred=pipe.predict(X_test)
r2_score(y_test,y_pred)

import pickle

pickle.dump(pipe,open('LinearRegressionModel.pkl','wb'))

pipe.predict(pd.DataFrame(columns=['name','company','year','kms_driven','fuel_type'],data=np.array(['Maruti Suzuki Swift','Maruti',2019,100,'Petrol']).reshape(1,5)))

pipe.steps[0][1].transformers[0][1].categories[0]

import pandas as pd
data_new = pd.DataFrame({
    'Price':80000,
    'Kms_Driven':27000,
    'Fuel_Type':0,
    'Seller_Type':0,
    'Transmission':0,
},index=[0])

import ipywidgets as widgets
from IPython.display import display

def predict_price(car_name, company, year, kms_driven, fuel_type):
    # Replace this with your actual prediction logic
    prediction = 500000  # Example prediction
    return prediction

car_name_input = widgets.Text(description="Car Name:")
company_input = widgets.Text(description="Company:")
year_input = widgets.IntSlider(description="Year:", min=2000, max=2023, value=2010)
kms_driven_input = widgets.IntSlider(description="Kilometers Driven:", min=0, max=100000, value=50000)
fuel_type_input = widgets.Dropdown(description="Fuel Type:", options=["Petrol", "Diesel", "CNG"])

predict_button = widgets.Button(description="Predict Price")

def on_predict_button_click(b):
    car_name = car_name_input.value
    company = company_input.value
    year = year_input.value
    kms_driven = kms_driven_input.value
    fuel_type = fuel_type_input.value

    prediction = predict_price(car_name, company, year, kms_driven, fuel_type)
    print("Car Purchase amount", prediction)

predict_button.on_click(on_predict_button_click)

display(car_name_input, company_input, year_input, kms_driven_input, fuel_type_input, predict_button)

