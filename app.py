#app.py
# %% [markdown]
# In this file, the prices of vehicles will be analyzed. It will be determined if the price of vehicles is affected by a variety of characteristics. The vehicles that will be analyzed will come from 19 different brands, but will only be vehicles sold in the United States.

# %%
import pandas as pd
import numpy as np
import streamlit as st

# %% [markdown]
# Reading the info on the data, it's very clear that there are several empty cells in this data that will need to be filled. Also, the date posted column needs to be converted to a datetime object. The model_year should be an integer, not a float.

# %%
data = pd.read_csv('vehicles_us.csv')
print(data.info())


# %%
data['model_year'] = data['model_year'].fillna(data['model_year'].median())
data['cylinders'] = data.groupby('model')['cylinders'].fillna(data['cylinders'].median())
data['odometer'] = data.groupby('model')['odometer'].fillna(data['odometer'].median())
data['is_4wd'] = data.groupby('model')['is_4wd'].fillna(0)
data['paint_color'] = data['paint_color'].fillna('Unknown')
data['date_posted'] = pd.to_datetime(data['date_posted'],format='%Y-%m-%d')
data['model_year'] = data['model_year'].astype('int64')
print(data.info())

# %% [markdown]
# Now, it's time to search for obvious duplicated rows in the data. Since many of these cars from the same brands have equal features, duplicates will be looked for by date_posted, days_listed, price, and odometer. If two cars have these key features the same, they will be assumed duplicates.

# %%
print(data[data.duplicated()].count())

# %%
print(data['condition'].unique())

# %%
print(data.shape)

# %% [markdown]
# The model names are a little lengthy. I will create a function that gets the specific brand of these vehicles. 

# %%
def get_brands(df):
    return str.split(df['model'],sep=' ')[0]
    

# %%
#Most popular sold brands
data['brands'] = data.apply(get_brands,axis=1)
print(data['brands'].nunique())
print(data.groupby('brands')['brands'].count().sort_values(ascending=False))

# %% [markdown]
# Now it's time to create the streamlit app. Start with the header, and tell the user to choose a brand to check prices.

# %%
st.header("Market of used cars. Original data")
st.write("""
         Filter the data below to see the listed prices by manufacturers.
         """)
show_new_cars = st.checkbox('Include new cars from dealers',value=True)


# %%
show_new_cars

# %%
if not show_new_cars:
    data = data[data['condition']!='like new']

# %%
manufacturer_choice = data['brands'].unique()

# %%
make_choice_brand = st.selectbox('Select Manufacturer:',manufacturer_choice)

# %%
print(make_choice_brand)

# %%
min_year,max_year = (data['model_year'].min() , data['model_year'].max())
year_range = st.slider(label='Choose year',min_value=data['model_year'].min(),max_value=data['model_year'].max(),value=(min_year,max_year))

# %%
print(year_range)

# %%
actual_range = list(range(year_range[0],year_range[1]+1))
print(actual_range)

# %%
filtered_type = data[(data['brands']==make_choice_brand) & (data['model_year'].isin(list(actual_range)))]
st.table(filtered_type.head(10))

# %%
print(filtered_type)

# %%
st.header('Price Analysis')
st.write("""
Let's see what influences price the most. We can analyze this by comparing transmission, condition, miles, and days listed.""")

import plotly.express as px

list_for_histogram = ['condition','transmission','odometer','days_listed']
choice_for_histogram = st.selectbox('Split for Price Distribution',list_for_histogram)
histogram_1 = px.histogram(data , x='price' , color=choice_for_histogram)
histogram_1.update_layout(title="<b> Split of price by {}<b>".format(choice_for_histogram))
st.plotly_chart(histogram_1)

# %%
#histogram_1.show()

# %%
data['age'] = 2023 - data['model_year']

def age_category(age):
    if(age < 5):return '<5'
    elif(age >= 5 and age < 10):return '5-10'
    elif(age >= 10 and age < 20):return '10-20'
    else:return '>20'
data['age_category'] = data['age'].apply(age_category)

# %%
print(data['age_category'])

# %%
st.write("""
#### Let's see how price is affected by the number of miles on the car, paint color, or if it's 4 wheel drive.""")

list_for_scatter = ['age','odometer','age_category']
choice_for_scatter = st.selectbox('Price dependency on ',list_for_scatter)
scatter_2 = px.scatter(data , x='price' , y=choice_for_scatter , hover_data=['model_year'])
scatter_2.update_layout(title="<b> Price vs {}<b>".format(choice_for_scatter))
st.plotly_chart(scatter_2)

# %%
#scatter_2.show()

# %% [markdown]
# In conclusion, one of the biggest things that affects the price of a vehicle is the number of miles on it. The more miles a car has, the less valuable it is. The older a car is, it will go down in value, until a certain age, about 60, then it goes up in value. However, the outlier vehicles that are 80+ years old. lose some of their antique value. The condition of the car has some effect the price of the vehicle.


