#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st


# In[2]:


data = pd.read_csv('vehicles_us.csv')
print(data.head())


# In[3]:

data['model_year'] = data['model_year'].fillna(data['model_year'].median())
data['cylinders'] = data.groupby('model')['cylinders'].ffill(data['cylinders'].median())
data['odometer'] = data.groupby('model')['odometer'].ffill(data['odometer'].median())
data['is_4wd'] = data.groupby('model')['is_4wd'].ffill(0)
data['paint_color'] = data['paint_color'].fillna('Unknown')
data['date_posted'] = pd.to_datetime(data['date_posted'],format='%Y-%m-%d')
data['model_year'] = data['model_year'].astype('int64')
print(data.info())

# In[4]:


print(data['condition'].unique())


# In[5]:


print(data.shape)


# In[6]:


def get_brands(df):
    return str.split(df['model'],sep=' ')[0]
    


# In[7]:


#Most popular sold brands
data['brands'] = data.apply(get_brands,axis=1)
print(data['brands'].nunique())
print(data.groupby('brands')['brands'].count().sort_values(ascending=False))


# In[8]:


st.header("Market of used cars. Original data")
st.write("""
         Filter the data below to see the ads by manufacturer
         """)
show_new_cars = st.checkbox('Include new cars from dealers')


# In[9]:


show_new_cars


# In[10]:


if not show_new_cars:
    data = data[data['condition']!='like new']


# In[11]:


manufacturer_choice = data['brands'].unique()


# In[12]:


make_choice_brand = st.selectbox('Select Manufacturer:',manufacturer_choice)


# In[13]:


print(make_choice_brand)


# In[14]:


min_year,max_year = (data['model_year'].min() , data['model_year'].max())
year_range = st.slider(label='Choose year',min_value=min_year,max_value=max_year)

# In[15]:


print(year_range)


# In[16]:


actual_range = list(range(year_range[0],year_range[1]+1))
print(actual_range)


# In[17]:


filtered_type = data[(data['brands']==make_choice_brand) & (data['model_year'].isin(list(actual_range)))]
st.table(filtered_type.sample(10))


# In[18]:


print(filtered_type.sample(10))


# In[19]:


st.header('Price Analysis')
st.write("""
Let's see what influences price the most. We can analyze this by comparing transmission, condition, miles, and days listed.""")

import plotly.express as px

list_for_histogram = ['transmission','condition','odometer','days_listed']
choice_for_histogram = st.selectbox('Split for Price Distribution',list_for_histogram)
histogram_1 = px.histogram(data , x='price' , color=choice_for_histogram)
histogram_1.update_layout(title="<b> Split of price by {}<b>".format(choice_for_histogram))
st.plotly_chart(histogram_1)


# In[20]:

histogram_1.show()


# In[21]:


data['age'] = 2023 - data['model_year']

def age_category(age):
    if(age < 5):return '<5'
    elif(age >= 5 and age < 10):return '5-10'
    elif(age >= 10 and age < 20):return '10-20'
    else:return '>20'
data['age_category'] = data['age'].apply(age_category)


# In[22]:


print(data['age_category'].head())


# In[23]:


st.write("""
#### Let's see how price is affected by the number of miles on the car, paint color, or if it's 4 wheel drive.""")

list_for_scatter = ['odometer','age','age_category']
choice_for_scatter = st.selectbox('Price dependency on ',list_for_scatter)
scatter_2 = px.scatter(data , x='price' , y=choice_for_scatter , hover_data=['model_year'])
scatter_2.update_layout(title="<b> Price vs {}<b>".format(choice_for_scatter))
st.plotly_chart(scatter_2)


# In[24]:


scatter_2.show()


# In[ ]:



