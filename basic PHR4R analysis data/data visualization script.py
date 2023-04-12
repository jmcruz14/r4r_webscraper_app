# data visualization script

#%%
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import re
sns.set_theme(style='darkgrid')

weekdates = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

requests_with_males = ['M4A', 'M4F', 'M4M', 'F4M', 'F4A', 'F4F']
requests_females_only = ['F4F', 'F4M', 'F4A']
requsts_males_only = ['M4A', 'M4F', 'M4M']
f4m_only = ['F4M']

# Read Excel
df = pd.read_excel("reddit_posts.xlsx", "Information")

# Clean data
df['Request'] = df['Request'].astype(str)
df['Age'] = df['Age'].astype(str)
age_mask = (df['Age'].str.len() == 2)
df['Age'] = df['Age'].loc[age_mask]

# Remove null
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df['Age'] = df['Age'].astype(str)
df['Age'] = df['Age'].apply(lambda x:x[0:2])

# Between brackets only
in_bracket = r'.*?\[(.*)\].*'
df['Request'] = df['Request'].apply(lambda x:re.search(in_bracket, x).group(1))

# Capitalize Requests
df['Request'] = df['Request'].map(lambda x : x.upper())

# Split into Day and Time
df['Day'] = [d.date() for d in df['Date Time']]
df['Time'] = [d.time() for d in df['Date Time']]
df.drop('Date Time', inplace = True, axis = 1)
df['Day'] = pd.to_datetime(df.Day, format='%Y-%m-%d') # Convert to datetime object
df['Day'] = df['Day'].dt.day_name()

# Split Time Further Into Military Time
df['Time'] = df['Time'].astype(str)
df[['Hour', 'Minute', 'Second']] = df['Time'].str.split(':', expand=True)
df.drop(['Time', 'Second'], axis=1, inplace=True)
df['Hour'] = df['Hour'].astype(int)
df['Minute'] = df['Minute'].astype(int)

# Remove Duplicates
df.drop_duplicates(['Age', 'Request', 'Title'], inplace = True)

# Separating into request types – WITH MALES AND FEMALES
## EDIT THIS TO CHANGE THE SCOPE OF THE STUDY
def label_requests(row):
    if row['Request'] in f4m_only:
        return row['Request']
    else:
        return 'Others'

df['Requests_adjusted'] = df.apply(lambda row: label_requests(row), axis=1)
print(df)
#%%
# Age Request Count
df_2 = df.groupby(['Age'])['Age'].size().reset_index(name='Count')
df_2.drop(28, inplace=True)

#%%

# Age-Count Table
# sns.barplot(data=df_2, x='Age', y='Count')
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# ax.set_title('Age Distribution of R4R Users')
# ax.bar(df_2['Age'],df_2['Count'])
# plt.xticks(fontsize=10)

# # Request Size Table
# df_3 = df.groupby(['Requests_adjusted'])['Requests_adjusted'].size().reset_index(name='Count')
# df_3.sort_values('Count', inplace=True, ascending=False)
# fig_2 = plt.figure()
# ax_2 = fig_2.add_axes([0,0,1,1])
# ax_2.set_title('Requests')
# ax_2.bar(df_3['Requests_adjusted'],df_3['Count'])
# plt.xticks(fontsize=10)

# Barplot with continuous hues and sizes needed
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

df.drop(df[df.Requests_adjusted == 'Others'].index, inplace=True)
df_4 = df.groupby(['Day', 'Requests_adjusted'])['Day', 'Requests_adjusted'].size().reset_index(name='Count')

print(df_4)

print(df_4['Day' == "Monday"])

sns.set_theme(style="darkgrid")
sns.set(rc={'figure.figsize':(15,15)})
g = sns.catplot(data=df_4, kind='bar', x='Day', 
            y='Count', hue='Requests_adjusted', palette='coolwarm_r')
g.despine(left=True)
g.set_axis_labels("Day", "Count")
g.legend.set_title('Request Type')
plt.title("Requests Per Day")
plt.xticks(fontsize=8)

#%%
# Scatterplot for Monday to Sunday
# days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# fig_3, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(1, 7)
# fig_3.suptitle("R4R Requests Per Day")
# sns.set_theme(style='ticks')

#%%

# Scatterplot of post frequency of F4M posts in a week
df_5 = df.groupby(['Requests_adjusted', 'Day', 'Hour', 'Minute'])['Requests_adjusted', 'Day', 'Hour', 'Minute'].size().reset_index(name='Count')
df_5['Hour'] = df_5['Hour'].astype(int)
df_5['Minute'] = df_5['Minute'].astype(int)

g = sns.catplot(data=df_5, col='Day', x='Hour', y='Minute', kind='swarm',
    palette='cool')
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle('F4M Requests Per Day')
plt.xticks(fontsize=10)

# FacetGrid is multiple plots
# g = sns.FacetGrid(df_5, row="Day", margin_titles=True)
# g.map(sns.relplot, "Hour", "Minute", 'Requests_adjusted', "Count",
#     palette='cool', height = 6.5, aspect=.80)
# g.savefig("days_of_week.png")

# sns.set_theme(style='ticks')
# f, ax_3 = plt.subplots(figsize=(6.5, 8))
# sns.scatterplot(data=df, x='Hour', y='Minute', hue='Requests_adjusted', 
#                 sizes=(1, 1), linewidth=0, ax = ax_3, palette="ch:r=-.2,d=.3_r")

#%%

# Group into Age and Day
# df = df.groupby(['Day']).get_group('Sunday')
# print(df)

# Per plot graph is one day of the week
# each bar graph: count along y-axis and time of day along the x-axis

# additional variable: age of user
# focus of study: F4X

# CHECK FOR GRAPHS SORTED ACCORDING TO DAY OF THE WEEK