import re
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
from collections import Counter

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    num_messages = df.shape[0]
    
    words = []
    for message in df['message']:
        # Remove punctuation and split into words
        words.extend(message.split(sep="  "))
    
 
    
    # """Old code"""
    # # if selected_user == 'Overall':
    # #     # Filter out group notifications
    # #     filtered_df = df[df['user'] != 'group_notification']
    # #     num_messages = df.shape[0]
        
    # #     # Count words only in actual messages
    # #     words = []
    # #     for message in filtered_df['message']:
    # #         # Remove punctuation and split into words
    # #         cleaned_message = re.sub(r'[^\w\s]', '', message)
    # #         words.extend(cleaned_message.split())
    # #     return num_messages, len(words)
    
    # # else:
    # #     new_df = df[df['user'] == selected_user]
    # #     num_messages = new_df.shape[0]
        
    # #     # Count words only if it's not a group notification
    # #     words = []
    # #     if selected_user != 'group_notification':
    # #         for message in new_df['message']:
    # #             cleaned_message = re.sub(r'[^\w\s]', '', message)
    # #             words.extend(cleaned_message.split())
    # #     return num_messages, len(words)
        
        
    # fetch the number of media messages
    num_media = df[df['message'] == '< M e d i a   o m i t t e d > \n'].shape[0]
    
    # fetch the number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    
    return num_messages, len(words),num_media, len(links)

# Fetch most busy users
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
    columns={'index': 'name', 'user': 'percent'})
    return x,df

# wordcloud
def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '< M e d i a   o m i t t e d >\n']



    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
   
    df_wc = wc.generate(df['message'].str.cat(sep="  "))
    return df_wc

# Emoji analysis
def create_emoji(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    # emoji_df = emoji_df.rename(columns={0: 'Emoji', 1: 'Count'})
 
    return emoji_df

#Timeline
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
