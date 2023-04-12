#%%
import pandas as pd
import praw
from datetime import datetime
import time
import numpy as np
# import matplotlib.pyplot as plt
# sns.set_theme(style="white", context="talk")
import sys

import os
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

#%%
# import seaborn as sns

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return datetime.utcfromtimestamp(utc_datetime) + offset

reddit = praw.Reddit(
    client_id='8NDN4K63_ddqb_3-zfwqxQ', 
    client_secret='PpiZVrY7muqEk2xlKXstg502NUmiwA', 
    user_agent='PHR4R Web Scraping Application',
    username = 'entrity_screamr',
    password = 'Gk21bbaDK01')
#%%

new_posts = reddit.subreddit('phr4r').new()

post_info = []

for post in new_posts:
    post_info.append([post.title, datetime_from_utc_to_local(post.created_utc)])

pd_post = pd.DataFrame(post_info, columns=['Title', 'Date Time'])
pd_post[['Age', 'Request', 'Title']] = pd_post['Title'].str.split(' ', expand=True, n=2) # Split the columns into parts
pd_post = pd_post[['Age', 'Request', 'Title', 'Date Time']] # Rearrange the columns into proper order

read_df = pd.read_excel('reddit_posts.xlsx', sheet_name='Information')

unduplicated_df = pd.concat([pd_post, read_df]).drop_duplicates(['Title', 'Date Time'], keep=False) # Remove overlapping entries

# Remove entries from the reddit_posts file that already exist
unduplicated_df = unduplicated_df.merge(pd_post, on=['Title', 'Date Time'], how='left', copy=False)
unduplicated_df = unduplicated_df.dropna(how='any')
unduplicated_df = unduplicated_df.drop_duplicates(['Title', 'Date Time']) 
unduplicated_df.columns = unduplicated_df.columns.str.strip('_x')
unduplicated_df.columns = unduplicated_df.columns.str.strip('_y')
if unduplicated_df.shape[0]:
    unduplicated_df = unduplicated_df.loc[:,~unduplicated_df.T.duplicated(keep='first')]
   
    # with pd.ExcelWriter('reddit_posts.xlsx', mode='a', if_sheet_exists = 'overlay') as writer:  
    #     unduplicated_df.to_excel("reddit_posts.xlsx", sheet_name='Information', startrow=read_df.shape[0], index=False, header=False)

    # pd_post.to_excel("reddit_posts_test.xlsx", sheet_name='Information', index=False, header = True)

    # create excel file
    if os.path.isfile("reddit_posts.xlsx"):  # if file already exists append to existing file
        workbook = openpyxl.load_workbook("reddit_posts.xlsx")  # load workbook if already exists
        sheet = workbook['Information']  # declare the active sheet 

        # append the dataframe results to the current excel file
        for row in dataframe_to_rows(unduplicated_df, header = False, index = False):
            sheet.append(row)
        workbook.save("reddit_posts.xlsx")  # save workbook
        workbook.close()  # close workbook
    else:  # create the excel file if doesn't already exist
        with pd.ExcelWriter(path = "reddit_posts.xlsx", engine = 'openpyxl') as writer:
            unduplicated_df.to_excel(writer, index = False, sheet_name = 'Information')
else:
    sys.exit()


# Update script to run every x hours
# Doesn't include duplicate usernames, only age-sex-title-time
# startrow = read_df.shape[0]
# Stop once an entire week's worth of data has been collected
# Merge similar titles when done