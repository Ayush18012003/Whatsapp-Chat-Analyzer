import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    # Number of messages
    num_messages = df.shape[0]

    # Number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def Most_Engaged_User(df):
    x = df['user'].value_counts().head()
    percent_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'}
    )
    return x, percent_df


def creating_worldCloud(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(df['message'].str.cat(sep=" "))


def commonly_used_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def emoji_analysis(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


def monthly_timeline(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    return df.groupby('only_date').count()['message'].reset_index()


def week_activity_map(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    # Create pivot table for the heatmap
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    # Sort rows (days) for a more logical sequence
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    user_heatmap = user_heatmap.reindex(day_order)

    return user_heatmap

