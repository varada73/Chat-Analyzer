import re

from fontTools.varLib.plot import stops
from pandas import value_counts
from pygments.lexer import words
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extractor=URLExtract()
def fetchstats(user_type, df):

        # Filter by user if not 'Overall'
        if user_type != 'Overall':
            df = df[df['User'] == user_type]

        # Count the number of messages
        num_message = df.shape[0]

        # Count total words in the messages
        num_words = df['Message'].str.split().str.len().sum()

        num_mm=df[df['Message']=='<Media omitted>'].shape[0]

        links=[]
        for message in df['Message']:
                links.extend(extractor.find_urls(message))


        return num_message, num_words, num_mm, len(links)

def most_active_users(df):
        x=df['User'].value_counts().head(5)

        df=round((df['User'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name' ,'User':'Percent Use'})

        return x,df


def create_wc(selected_user,df):
        if selected_user!='Overall':
                df=df[df['User'] == selected_user]

        wc=WordCloud(width=800, height=600, background_color='white',min_font_size=10)
        df_wc=wc.generate(df['Message'].str.cat(sep=' '))
        return df_wc

def most_common_words(selected_user,df):
        f=open('stop_hinglish.txt','r')
        stop_words=f.read().split('\n')
        if(selected_user!='Overall'):
                df=df[df['User'] == selected_user]

        temp=df[df['User']!='Group Notification']
        temp=temp[temp['Message']!='<Media omitted>']

        words=[]
        for message in temp['Message']:
                for word in message.lower().split():
                        if word not in stop_words:
                                words.append(word)

        mw_df=pd.DataFrame(Counter(words).most_common(20))
        return mw_df

def analyze_emoji(selected_user,df):
        if selected_user!='Overall':
                df=df[df['User'] == selected_user]

        emojis=[]
        for message in df['Message']:
                emojis.extend([c for c in message if emoji.is_emoji(c)])

        me_df=pd.DataFrame(Counter(emojis).most_common(20))
        return me_df

def monthly_timeline(selected_user,df):
        if selected_user!='Overall':
                df=df[df['User'] == selected_user]
        timeline=df.groupby(['Year','Month']).count()['Message'].reset_index()

        time=[]
        for i in range(timeline.shape[0]):
                time.append(timeline['Month'][i]+'-'+str(timeline['Year'][i]))
        timeline['time']=time
        return timeline

def week_map(selected_user,df):
        if selected_user!='Overall':
                df=df[df['User'] == selected_user]
        df['day_name']=df['date and time'].dt.day_name()
        return df['day_name'].value_counts()