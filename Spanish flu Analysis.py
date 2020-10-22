# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:12:44 2020

@author: Edwyn
"""
#Importing necessary libraries
import pandas as pd 
import os
import calendar
import seaborn as sns
sns.set()
sns.set_palette("pastel")
import matplotlib.pyplot as plt


#This is to change current working directory to a particular path
os.chdir('C:\\Users\\Edwyn\\Desktop\\PROJECT\\')

#setting up max number of columns and rows that can be displayed
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',2000)


#Names of csv files to read from URl saved in 2 variables:
file_1 = 'Gold.csv'
file_2 = 'S_P_500.csv'
file_3 = 'WTI_Oil.csv'
file_5 = 'Pandemic.csv'

#path to write csv to
path='C:\\Users\\Edwyn\\Desktop\\PROJECT\\'



#Storing csv files into file handle
df_gold = pd.read_csv('Gold.csv',low_memory = False)
df_gold

df_500 = pd.read_csv('S_P_500.csv',low_memory = False)
df_500

df_wti_oil = pd.read_csv('WTI_Oil.csv',low_memory = False)
df_wti_oil

df_cases = pd.read_csv('Pandemic.csv',encoding= 'unicode_escape')
df_cases



#checking missing values
df_gold.count()
df_500.count()
df_wti_oil.count()

#Checking data types
df_gold.dtypes
df_wti_oil.dtypes
df_500.dtypes
df_cases.dtypes

#Joining gold dataset to oil dataset and filling in the missing values..storing that as df_1
df_1 = df_gold.merge(df_wti_oil, how = 'inner',on = 'Date')
df_1.columns=['Date','Gold_price','WTI_crude_price']
df_1['WTI_crude_price'].fillna(0, inplace=True)
df_1['Gold_price'].fillna(0, inplace=True)
df_1.head(100)
df_1.count()

#Joining df_1 dataset to S&P 500 dataset and filling in the missing values....storing that as df_2
df_2= df_1.merge(df_500, how = 'left',on = 'Date')
df_2.columns=['Date','Gold_price','WTI_crude_price','S&P_index']
df_2['WTI_crude_price'].fillna(0, inplace=True)
df_2['Gold_price'].fillna(0, inplace=True)
df_2['S&P_index'].fillna(0, inplace=True)
df_2
df_2.count()


#Joining df_2 dataset to pandemic records dataset and filling in the missing values....storing that as df_total
df_total = df_2.merge(df_cases, how = 'left',left_on = 'Date',right_on = 'Date')
df_total['Cases'].fillna(0, inplace=True)
df_total['Deaths'].fillna(0, inplace=True)
df_total['WTI_crude_price'].fillna(0, inplace=True)
df_total['Gold_price'].fillna(0, inplace=True)
df_total['S&P_index'].fillna(0, inplace=True)

#Extracting month year and weekdays from the date column
df_total['Year'] = pd.to_datetime(df_total['Date']).dt.year
df_total['Month'] = pd.to_datetime(df_total['Date']).dt.month
df_total['Day'] = pd.to_datetime(df_total['Date']).dt.weekday
df_total = df_total[df_total['Month'].notna()]
df_total

#Converting Month from number to actual name of the month
df_total['Month'] = df_total['Month'].apply(lambda x: calendar.month_abbr [x])

#Converting days from number to actual name of the day
df_total['Day'] = df_total['Day'].apply(lambda x: calendar.day_abbr [x])

#Displaying the data
df_total.head(1000)

#Filling missing country nulls with most common occuring country
df_total['Country'].fillna(df_total['Country'].value_counts().index[0],inplace=True)
df_total

#Checking for nulls
df_total.isnull().sum()

#printing final output to csv
df_total.to_csv('mergedd.csv')


#Generating Heatmap
corrMatrix =df_total.corr()
corrMatrix
sns.heatmap(corrMatrix, annot=True,cmap = 'coolwarm')
plt.show()


#slicing years from which pandemic started to when it ended officially as declared by WHO
start = (df_total[df_total['Date']=='4/17/2009'].index.values)
start
end = (df_total[df_total['Date']=='8/11/2010'].index.values)
end                             
df_pandemic = df_total.loc[5776:6103,['Date','Gold_price','WTI_crude_price','S&P_index','Cases','Deaths','Year','Month']]
df_pandemic.tail()

#Slicing years for analysis based on two years before start of pademic and two years after pandemic
year_start = (df_total[df_total['Date']=='1/2/2007'].index.values)
year_start
year_end = (df_total[df_total['Date']=='12/12/2012'].index.values)
year_end
df_analysis = df_total.loc[5208:6680,['Date','Gold_price','WTI_crude_price','Country','S&P_index','Cases','Deaths','Year','Month']]
df_analysis

#Checking data types
df_analysis.dtypes

#Converting date from object to datetime datatype
df_analysis['Date'] = pd.to_datetime(df_analysis['Date'])
df_pandemic['Date'] = pd.to_datetime(df_pandemic['Date'])
df_analysis.head()

#Performing Exploratory Data Analysis
df_analysis['Gold_price'].mean()
df_analysis['S&P_index'].mean()
df_analysis['WTI_crude_price'].mean()

df_analysis['Gold_price'].hist()
plt.xlabel('Gold_Price $/Oz')
plt.show()

df_analysis['S&P_index'].hist()
plt.xlabel('S*P_index')
plt.show()

df_analysis['WTI_crude_price'].hist()
plt.xlabel('WTI_oil_Price $/bbl')
plt.show()

#Line plot for Gold against Years
fig1,ax = plt.subplots()
ax.plot(df_analysis['Date'],df_analysis['Gold_price'],'y--', label = 'Gold prices')
ax.set_ylabel('Gold_Price $/Oz')
ax.set_xlabel('Years')
ax.set_title('Gold price line plot')
ax.legend()
plt.show()

#Line plot for Oil against Years
fig2,ax2 = plt.subplots()
ax2.plot(df_analysis['Date'],df_analysis['WTI_crude_price'],'g--', label = 'US oil price')
ax2.set_ylabel('WTI_oil_Price $/bbl')
ax2.set_xlabel('Month')
ax2.set_title('Oil price line plot')
ax2.legend()
plt.show()

#Line plot for S&P index against Years
fig3,ax3 = plt.subplots()
ax3.plot(df_analysis['Date'],df_analysis['S&P_index'],'royalblue', label = 'S&P_index')
ax3.set_ylabel('S&P index')
ax3.set_xlabel('Month')
ax3.set_title('S&P_index line plot')
ax3.legend()
plt.show()

#Scatter plot for Oil against Gold during pandemic
fig4,ax4=plt.subplots()
ax4.scatter(x=df_pandemic['WTI_crude_price'], y=df_pandemic['Gold_price'],color= 'darkviolet')
ax4.legend(labels=['Oil price', 'Gold_price'])
ax4.set_xlabel('Oil price $/bbl')
ax4.set_ylabel('Gold_price $/Oz')
ax4.set_title("Cases vs Gold_price scatter plot")
plt.show()

#Scatter plot for S&P index against Gold during pandemic
fig5,ax5=plt.subplots()
ax5.scatter(x=df_pandemic['Gold_price'], y=df_pandemic['S&P_index'],color= 'slategray')
ax5.legend(labels=['Gold price', 'S&P_index'])
ax5.set_xlabel('Gold price $/Oz')
ax5.set_ylabel('S&P_index')
ax5.set_title("Gold price vs S&P_index scatter plot")
plt.show()

#Scatter plot for S&P index against Oil during pandemic
fig6,ax6=plt.subplots()
ax6.scatter(x=df_pandemic['S&P_index'], y=df_pandemic['WTI_crude_price'],color= 'lightskyblue')
ax6.legend(labels=['S&P_index', 'WTI_crude_price'])
ax6.set_xlabel('S&P_index')
ax6.set_ylabel('WTI_crude_price $/bbl')
ax6.set_title("S&P_index vs WTI_crude_price scatter plot")
plt.show()


