import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
from collections import Counter
def fetch_stats(selected_user,df) :
    if selected_user != "Total Group":
        df = df[df['User'] == selected_user]

    # Fetch Number of Messages
    num_msgs = df.shape[0]

    # Find All tDe wNrds
    words = []
    for msg in df['Message']:
        words.extend(msg.split())

    # Find Number of Media Files
    medias = df[df['Message']=='<Media omitted>\n'].shape[0]

    # Find Number of Links
    links = []
    extractor = URLExtract()
    for msg in df['Message']:
        links.extend(extractor.find_urls(msg))

    return num_msgs, words, medias,links
def most_busy_users(df):
    chat_percentage = round(df['User'].value_counts() / df.shape[0], 3).reset_index()
    chat_percentage.columns = ['User', 'Percentage']
    return df['User'].value_counts().head(), chat_percentage
def least_busy_users(df) :
    return df['User'].value_counts().tail()

def create_wordcloud(selected_user, df):
    if selected_user != "Total Group":
        df = df[df['User'] == selected_user]
    df = df[df['Message'] != '<Media omitted>\n']
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))
    return df_wc
def most_commom_words(selected_user, df):
    if selected_user != "Total Group":
        df = df[df['User'] == selected_user]
    pure_df = df[df['User'] != 'notification']
    pure_df = pure_df[pure_df['Message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r', encoding='utf-8')
    stop_words = f.read()
    stop_words = stop_words.split('\n')
    words = []
    for msg in pure_df['Message']:
        for word in msg.lower().split():
            if (word not in stop_words and len(word)!=1):
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))
def emoji_func(selected_user, df):
    if selected_user != "Total Group":
        df = df[df['User'] == selected_user]
    emojis = []
    for msg in df['Message']:
        emojis.extend([c for c in msg if emoji.is_emoji(c)])
    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojidf

def analyze_with_time(selected_user , df):
    if selected_user != "Total Group":
        df = df[df['User'] == selected_user]
    time_df = df.groupby(['Year', 'Month', 'Month_Num']).count()['Message'].reset_index()
    time_df = time_df.sort_values(['Year', 'Month_Num'])
    time_df = time_df.reset_index(drop=True)
    times = []
    for i in range(len(time_df)):
        times.append(str(time_df['Year'][i]) + '-' + str(time_df['Month'][i]))
    time_df['Time'] = times
    return time_df

def week_activity_map(selected_user,df):
    if selected_user != "Total Group":
        df = df[df['User'] == selected_user]
    return df['Day_Name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != "Total Group":
        df = df[df['User'] == selected_user]
    return df['Month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != "Total Group":
        df = df[df['User'] == selected_user]
    user_heatmap = df.pivot_table(index='Day_Name', columns='Period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap