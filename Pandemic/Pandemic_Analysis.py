# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 13:41:44 2020

@author: Edwyn
"""

import pandas as pd 
import os
import calendar
import seaborn as sns
import matplotlib.pyplot as plt

os.chdir('C:\\Users\\Edwyn\\Desktop\\PROJECT\\')

pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',2000)

#store URL in a variable

#Names of csv files to read from URl saved in 2 variables:
file_1 = 'Gold.csv'
file_2 = 'S_P_500.csv'
file_3 = 'WTI_Oil.csv'
file_4 = 'Brent_Oil.csv'
file_5 = 'Pandemic.csv'

#path to write csv to
path='C:\\Users\\Edwyn\\Desktop\\PROJECT\\'

df_gold = pd.read_csv('Gold.csv',low_memory = False)
df_gold

df_500 = pd.read_csv('S_P_500.csv',low_memory = False)
df_500

df_wti_oil = pd.read_csv('WTI_Oil.csv',low_memory = False)
df_wti_oil

df_brent_oil = pd.read_csv('Brent_Oil.csv',low_memory = False)
df_brent_oil

df_cases = pd.read_csv('Pandemic.csv',encoding= 'unicode_escape')
df_cases

#checking missing values
df_gold.count()
df_500.count()
df_wti_oil.count()
df_brent_oil.count()

df_gold.dtypes
df_wti_oil.dtypes
df_500.dtypes
df_brent_oil.dtypes
df_cases.dtypes


df_1 = df_gold.merge(df_wti_oil, how = 'inner',on = 'Date')
df_1.columns=['Date','Gold_price','WTI_crude_price']
df_1['WTI_crude_price'].fillna(0, inplace=True)
df_1['Gold_price'].fillna(0, inplace=True)
df_1.head(100)
df_1.count()

df_merge = df_1.merge(df_brent_oil, how = 'inner',left_on = 'Date',right_on = 'Date')
df_merge.columns=['Date','Gold_price','WTI_crude_price','Brent_price']
df_merge.head(100)
df_merge['WTI_crude_price'].fillna(0, inplace=True)
df_merge['Gold_price'].fillna(0, inplace=True)
df_merge['Brent_price'].fillna(0, inplace=True)
df_merge.count()


df_final= df_merge.merge(df_500, how = 'inner',on = 'Date')
df_final.columns=['Date','Gold_price','WTI_crude_price','Brent_price','S&P_index']
df_final['WTI_crude_price'].fillna(0, inplace=True)
df_final['Gold_price'].fillna(0, inplace=True)
df_final['Brent_price'].fillna(0, inplace=True)
df_final['S&P_index'].fillna(0, inplace=True)
df_final
df_final.count()


df_total = df_final.merge(df_cases, how = 'outer',left_on = 'Date',right_on = 'Date')
df_total['Cases'].fillna(0, inplace=True)
df_total['Deaths'].fillna(0, inplace=True)
df_total['WTI_crude_price'].fillna(0, inplace=True)
df_total['Gold_price'].fillna(0, inplace=True)
df_total['Brent_price'].fillna(0, inplace=True)
df_total['S&P_index'].fillna(0, inplace=True)
df_total['Year'] = pd.to_datetime(df_total['Date']).dt.year
df_total['Month'] = pd.to_datetime(df_total['Date']).dt.month
df_total['Day'] = pd.to_datetime(df_total['Date']).dt.weekday
df_total = df_total[df_total['Month'].notna()]
df_total

df_total['Month'] = df_total['Month'].apply(lambda
x: calendar.month_abbr [x])

df_total['Day'] = df_total['Day'].apply(lambda
x: calendar.day_abbr [x])


df_total.tail(1000)

df_total['Country'].fillna(df_total['Country'].value_counts().index[0],inplace=True)
df_total

df_total.isnull().sum()

#printing out to csv
df_total.to_csv('merged.csv')
                                                                              
                                          
#Generating visualizations such as histogram,corr matrix etc...
df_total['Gold_price'].hist()
df_total['WTI_crude_price'].hist()
df_total['Brent_price'].hist()
df_total['S&P_index'].hist()

#Heatmap
corrMatrix =df_total.corr()
corrMatrix
sns.heatmap(corrMatrix, annot=True,cmap = 'coolwarm')
plt.show()

#slicing years from which pandemic started to when it ended officially as declared by WHO
start = (df_total[df_total['Date']=='4/17/2009'].index.values)
start
end = (df_total[df_total['Date']=='8/11/2010'].index.values)
end

df_pandemic = df_total.loc[5414:5655,['Date','Gold_price','WTI_crude_price','Brent_price','S&P_index','Cases','Deaths','Year','Month']]
df_pandemic

#Two years before start of pademic

year_start = (df_total[df_total['Date']=='1/1/2007'].index.values)
year_start
year_end = (df_total[df_total['Date']=='12/12/2012'].index.values)
year_end


#Lineplots
fig = plt.figure()                                                               
ax = fig.add_subplot(1,1,1) 
plt.title('WTI_crude_price')
df_pandemic['Gold_price'].plot(linewidth=0.5)
years = plt.matplotlib.dates.YearLocator()
months = plt.matplotlib.dates.MonthLocator()
yearsFmt = plt.matplotlib.dates.DateFormatter('%Y')

ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)

ax.grid(which='both', axis='x')
plt.show()



plt.title('Cases')
sns.lineplot(df_pandemic['Date'], df_total['Cases'])

plt.title('Deaths')
sns.lineplot(df_total['Date'], df_total['Deaths'])

#Scatter matrix
pd.plotting.scatter_matrix(df_final)


ax8.xaxis.set_major_locator(years)
ax8.xaxis.set_major_formatter(years_fmt)
ax8.xaxis.set_minor_locator(months)
ax8.xaxis.set_minor_formatter(monthsFmt)
plt.setp(ax8.get_minorticklabels(), rotation=90)





