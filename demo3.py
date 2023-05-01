#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
#import numpy as np
#import altair as alt
#import pydeck as pdk
#import matplotlib.pyplot as plt
#from datetime import datetime,timedelta
import plotly.express as px

import seaborn as sns
sns.set()

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")



# LOADING DATA

DATA_URL = 'sythetic_data.csv'

st.title('Welcome')

#Caching data 

#@st.cache
def load_data():
    data = pd.read_csv(DATA_URL,parse_dates=['Period'])
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)    #convert col name to lowercase
    return data

data = load_data()

#SEARCH BAR

title = st.text_input('Query', 'Search Bar')
st.write('Search history:- ', title)


#--------SIDEBAR----------------
st.sidebar.title('Navigation')


charts=['Bar Chart','Scatter Chart','Line Chart']
chart_type=st.sidebar.selectbox('Chart type',charts)


domain=st.sidebar.multiselect('Industry/Domain',data['domain_new'].unique())
#Data Filtering
if domain:              
    data=data[data.domain_new.isin(domain)]


role=st.sidebar.multiselect('Job Role',data['role'].unique())
#Data Filtering
if role:               
    data=data[data.role.isin(role)]
    

skill=st.sidebar.multiselect('Skills',data['skill'].unique())
#Data Filtering
if skill:
    data=data[data.skill.isin(skill)]


period=st.sidebar.multiselect('Period',data['period'].dt.month.unique())
#Data Filtering
if period:
    data=data[data.period.dt.month.isin(period)]
#st.sidebar.date_input('Filter by Date',datetime.now())

company=st.sidebar.multiselect('Company',data['company_new'].unique())
#Data Filtering
if company:
    data=data[data.company_new.isin(company)]


st.sidebar.multiselect('Company Size',['1-50','51-200','200-500','500-1000','1000+'])


st.sidebar.slider('Salary',min_value=0, max_value=200, value=[0,50],format='$%sK')


st.sidebar.slider('Experience Required',min_value=0, max_value=10, value=[0,2])




#y_axis=st.sidebar.multiselect('Y-axis',data.columns)
st.sidebar.write('Y-axis aggregation')
agg = st.sidebar.radio("Aggregated by",('Count', 'Sum', 'Avg'))
#st.sidebar.multiselect('Pick one',data['role'].unique())


st.sidebar.write('Filters')
certi = st.sidebar.checkbox('Certification')
if certi:
    st.sidebar.selectbox('Certificate',['xyz','abc'])
    
recruit= st.sidebar.checkbox('Currently Recruiting')

#-------SIDEBAR----------------


#+++++++++PAGE+++++++++++


#Data Filtering

raw_data=data
#'Top 20 Skill needed for %s Role'%roles
if certi:
    "data=data[data['certifications'].notnull()].reset_index(drop=True)"    #REPLACE CODE
    

if recruit:
    "data=data[data['flag for recruitment']==True].reset_index(drop=True)"  #REPLACE CODE
    
    
#Chart selection



if chart_type:
    placeholder1 = st.empty()
    st.write('%s'%str(chart_type))
    placeholder1.write('### Industry Visualization')
   
    if chart_type=='Bar Chart':
        #st.write('barrrrr')
        
        #BAR PLOT
        
        
        #st.bar_chart(data['domain'].value_counts(),height=600)
                    
        if skill:
            placeholder1.empty()
            st.write('### Company Hiring Visualization')
            st.write('Selected Skills : %s'%skill)             
            if len(data['company'].value_counts()>80):
                st.bar_chart(data['company'].value_counts()[:80],height=550)
            else:
                st.bar_chart(data['company'].value_counts(),height=550)

        else:
            
        
            if role:
                placeholder1.empty()
                st.write('### Skills Visualization')
                st.write('Selected Roles : %s'%role) 
                if len(data['skill'].value_counts()>80):
                    st.bar_chart(data['skill'].value_counts()[:80],height=550)
                else:
                    st.bar_chart(data['skill'].value_counts(),height=550)
                
                st.write('### Company Hiring Visualization')
                if len(data['company'].value_counts()>80):
                    st.bar_chart(data['company'].value_counts()[:80],height=550)
                else:
                    st.bar_chart(data['company'].value_counts(),height=550)

                    
            else:
                if domain:
                    placeholder1.empty()
                    
                    
                    st.write('### Job Role Visualization')
                    st.write('Selected Domains : %s'%domain)  
                               
                    #data=data[data.domain_new.isin(domain)]
                    
                    #1st Chart
                    st.bar_chart(data['role'].value_counts(),height=550)
                    
                    fig1 = px.bar(
                        data['role'].value_counts().reset_index().rename(
                            columns={'index':'Job roles','role':'Counts'}).sort_values(by=['Job roles']),
                        x='Job roles', y='Counts', color='Job roles',height=750)
                    st.plotly_chart(fig1, use_container_width=True) 
                    
                    #2nd Chart
                    st.write('### Company Hiring Visualization')
                    if len(data['company'].value_counts()>80):
                        st.bar_chart(data['company'].value_counts()[:80],height=550)
                    else:
                        st.bar_chart(data['company'].value_counts(),height=550)
                else:
                    #st.bar_chart(data['domain'].value_counts(),height=550)
                    fig = px.bar(
                        data['domain'].value_counts().reset_index().rename(
                            columns={'index':'Industry','domain':'Counts'}).sort_values(by=['Industry']),
                        x='Industry', y='Counts', color='Industry',height=550)
                    st.plotly_chart(fig, use_container_width=True)        
                        
                    


            
        
            
            
            

        #if x_axis:
        #    if len(data['domain'].value_counts())>30:  #If there are lot of x-parameters
        #        st.bar_chart(data[str(x_axis[0])].value_counts()[:30],height=600)
        #    else: 
        #        st.bar_chart(data['domain'].value_counts()[:30],height=600)                    
        #        
        #else:
        #    'not barrrrrr'
    

    
    elif chart_type=='Scatter Chart':
        st.write('UNDER CONSTRUCTION')

    elif chart_type=='Line Chart':    
        #'UNDER CONSTRUCTION'
        
        placeholder1.empty()
        
        #st.line_chart(data['domain'].value_counts())        
        #st.write(data.groupby(['domain']).size())
        
        df=data.groupby(['domain','period']).size().reset_index().rename(columns={0:'Counts'})
        df['months']=df.period.dt.month
        fig3 = px.line(df, x="months", y="Counts",color='domain', title='Job posting history',line_dash='domain')
        st.plotly_chart(fig3, use_container_width=True)

    
    
#MANIPULATED DATA

if st.checkbox('Show Manipulated Data'):
    st.write(data.head())
    
    #DOWNLOAD BUTTON 
    
    #@st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    
    csv = convert_df(data)
    
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='download_manipulated_df.csv',
        )



#RAW DATA
if st.checkbox('Show Raw Data'):
    st.write('#### Raw Data',raw_data.head())
    
    #DOWNLOAD BUTTON 
    
    #@st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    
    csv1 = convert_df(raw_data)
    
    st.download_button(
        label="Download data as CSV",
        data=csv1,
        file_name='download_raw_df.csv',
        )

    
#SHOW SOURCE CODE
if st.checkbox('Show Source Code'):    
    fin = open("demo3.py", 'r')
    body = fin.read()
    st.code(body)


#+++++++PAGE+++++++++++++++




# In[ ]:




