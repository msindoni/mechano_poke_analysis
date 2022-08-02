import re
import math
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt
from matplotlib import pyplot as plt
from easygui import *
from scipy.optimize import curve_fit
from matplotlib.widgets import SpanSelector 
from iteration_utilities import grouper
from scipy.stats import pearsonr 

with open('Z:/All_Staff/Grandl Lab/Michael Sindoni/initial_frequency_screen/poke/initial_freq_screen_poke.csv', 'r') as fhand:
    df = pd.read_csv(fhand)

#add a normalized picoamp per picofarad for each cell. Only plan to use the max
df['pA/pf'] = df['current'] / df['capacitance']


#input what conditions are being analyzed
conditions = ['con', '10', '50', '200']

def max_current_box_plot(df, conditions): 
    condition_list = conditions
    conditions_dict = {}
    
    #generates items (key/value) in the conditions dictionary. The key is the condition and the value is an empty list
    for i in range(len(condition_list)):
        conditions_dict[condition_list[i]] = [] 

    #go through each trial, get max current, and add to correct value list in dictionary
    grouped = df.groupby(['condition', 'date', 'number'])
    for name, group in grouped:
        max_value = group['current'].max()
        ind_condition = name[0] #gets the condition
        conditions_dict[ind_condition].append(max_value) #appends list for that condition in the original dictionary

    #converts dictionary into a dataframe 
    df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in conditions_dict.items() ])).melt().dropna()

    #creating palette for box plot color scheme. Will correct for number of conditions with 8 being the max (con-200Hz)
    pal_colors = ['grey', '#464196', '#ffcfdc', 'maroon', 'goldenrod', 'navy', 'olivedrab', 'blueviolet']
    pal_dict = {}
    for i in range(len(condition_list)):
        pal_dict[conditions[i]] = pal_colors[i]
    sns.boxplot(data = df, x = 'variable', y = 'value', palette=pal_dict)
    sns.stripplot(data = df, x = 'variable', y = 'value', color = 'black')
    plt.ylim(0,)
    plt.show()

def pa_per_pf(df, conditions):
    condition_list = conditions
    conditions_dict = {}

    #generates items (key/value) in the conditions dictionary. The key is the condition and the value is an empty list
    for i in range(len(condition_list)):
        conditions_dict[condition_list[i]] = [] 

    #go through each trial, get max current, and add to correct value list in dictionary
    grouped = df.groupby(['condition', 'date', 'number'])
    for name, group in grouped:
        tau = group['pA/pf'].max()
        ind_condition = name[0] #gets the condition
        conditions_dict[ind_condition].append(tau) #appends list for that condition in the original dictionary

    #converts dictionary into a dataframe 
    df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in conditions_dict.items() ])).melt().dropna()

    #creating palette for box plot color scheme. Will correct for number of conditions with 8 being the max (con-200Hz)
    pal_colors = ['grey', '#464196', '#ffcfdc', 'maroon', 'goldenrod', 'navy', 'olivedrab', 'blueviolet']
    pal_dict = {}
    for i in range(len(condition_list)):
        pal_dict[conditions[i]] = pal_colors[i]
    sns.boxplot(data = df, x = 'variable', y = 'value', palette=pal_dict)
    sns.stripplot(data = df, x = 'variable', y = 'value', color = 'black')
    plt.ylim(0,)
    plt.show()

def tau_plot(df, conditions): 
    condition_list = conditions
    conditions_dict = {}
    
    #generates items (key/value) in the conditions dictionary. The key is the condition and the value is an empty list
    for i in range(len(condition_list)):
        conditions_dict[condition_list[i]] = [] 

    #go through each trial, get max current, and add to correct value list in dictionary
    grouped = df.groupby(['condition', 'date', 'number'])
    for name, group in grouped:
        tau = group['tau'].max()
        ind_condition = name[0] #gets the condition
        conditions_dict[ind_condition].append(tau) #appends list for that condition in the original dictionary

    #converts dictionary into a dataframe 
    df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in conditions_dict.items() ])).melt().dropna()

    #creating palette for box plot color scheme. Will correct for number of conditions with 8 being the max (con-200Hz)
    pal_colors = ['grey', '#464196', '#ffcfdc', 'maroon', 'goldenrod', 'navy', 'olivedrab', 'blueviolet']
    pal_dict = {}
    for i in range(len(condition_list)):
        pal_dict[conditions[i]] = pal_colors[i]
    sns.boxplot(data = df, x = 'variable', y = 'value', palette=pal_dict)
    sns.stripplot(data = df, x = 'variable', y = 'value', color = 'black')
    plt.ylim(0,)
    plt.show()

def pip_resistance(df, conditions):
    condition_list = conditions
    conditions_dict = {}

    #generates items (key/value) in the conditions dictionary. The key is the condition and the value is an empty list
    for i in range(len(condition_list)):
        conditions_dict[condition_list[i]] = [] 

    #go through each trial, get p50, and add to correct value list in dictionary
    grouped = df.groupby(['condition', 'date', 'number'])
    for name, group in grouped:
        pip_r = list(group['pip_r'])[0] #converts pandas core series to list and takes first element since they are all the same per group
        ind_condition = name[0] #gets the condition
        conditions_dict[ind_condition].append(pip_r) #appends list for that condition in the original dictionary


    #converts dictionary into a dataframe and creates box/strip plot
    df2 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in conditions_dict.items() ])).melt().dropna()

    #creating palette for box plot color scheme. Will correct for number of conditions with 8 being the max (con-200Hz)
    pal_colors = ['grey', '#464196', '#ffcfdc', 'maroon', 'goldenrod', 'navy', 'olivedrab', 'blueviolet']
    pal_dict = {}
    for i in range(len(condition_list)):
        pal_dict[conditions[i]] = pal_colors[i]
    sns.boxplot(data = df2, x = 'variable', y = 'value', palette=pal_dict)
    sns.stripplot(data = df2, x = 'variable', y = 'value', color = 'black')
    plt.ylim(0,)
    plt.show()

    #getting n for each category
    n_grouped = df2.groupby(['variable'])
    for name, group in n_grouped:
        len_category = len(group)
        print(name, ':', len_category)

def series_resistance(df, conditions):
    condition_list = conditions
    conditions_dict = {}

    #generates items (key/value) in the conditions dictionary. The key is the condition and the value is an empty list
    for i in range(len(condition_list)):
        conditions_dict[condition_list[i]] = [] 

    #go through each trial, get p50, and add to correct value list in dictionary
    grouped = df.groupby(['condition', 'date', 'number'])
    for name, group in grouped:
        series_r = list(group['series_r'])[0] #converts pandas core series to list and takes first element since they are all the same per group
        ind_condition = name[0] #gets the condition
        conditions_dict[ind_condition].append(series_r) #appends list for that condition in the original dictionary


    #converts dictionary into a dataframe and creates box/strip plot
    df2 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in conditions_dict.items() ])).melt().dropna()

    #creating palette for box plot color scheme. Will correct for number of conditions with 8 being the max (con-200Hz)
    pal_colors = ['grey', '#464196', '#ffcfdc', 'maroon', 'goldenrod', 'navy', 'olivedrab', 'blueviolet']
    pal_dict = {}
    for i in range(len(condition_list)):
        pal_dict[conditions[i]] = pal_colors[i]
    sns.boxplot(data = df2, x = 'variable', y = 'value', palette=pal_dict)
    sns.stripplot(data = df2, x = 'variable', y = 'value', color = 'black')
    plt.ylim(0,)
    plt.show()

def cell_capacitance(df, conditions):
    condition_list = conditions
    conditions_dict = {}

    #generates items (key/value) in the conditions dictionary. The key is the condition and the value is an empty list
    for i in range(len(condition_list)):
        conditions_dict[condition_list[i]] = [] 

    #go through each trial, get max current, and add to correct value list in dictionary
    grouped = df.groupby(['condition', 'date', 'number'])
    for name, group in grouped:
        capacitance = group['capacitance'].max()
        ind_condition = name[0] #gets the condition
        conditions_dict[ind_condition].append(capacitance) #appends list for that condition in the original dictionary

    #converts dictionary into a dataframe 
    df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in conditions_dict.items() ])).melt().dropna()

    #creating palette for box plot color scheme. Will correct for number of conditions with 8 being the max (con-200Hz)
    pal_colors = ['grey', '#464196', '#ffcfdc', 'maroon', 'goldenrod', 'navy', 'olivedrab', 'blueviolet']
    pal_dict = {}
    for i in range(len(condition_list)):
        pal_dict[conditions[i]] = pal_colors[i]
    sns.boxplot(data = df, x = 'variable', y = 'value', palette=pal_dict)
    sns.stripplot(data = df, x = 'variable', y = 'value', color = 'black')
    plt.ylim(0,)
    plt.show()



max_current_plot = max_current_box_plot(df,conditions) 
tau_plotx = tau_plot(df,conditions) 
normalized_current = pa_per_pf(df,conditions)
pip_resistances = pip_resistance(df, conditions) 
series_resistances = series_resistance(df, conditions) 
cell_capacitancex = cell_capacitance(df, conditions) 

print(df)
sns.pointplot(x = 'indentation',  y = 'current', data = df, hue = 'condition')
plt.show()

grouped = df.groupby(['condition', 'number'])
current_avg_list = []
mmHg_list = []
category_list = []
for group in grouped:
    df_iso = grouped[[]]
