import pandas as pd
from wordcloud import WordCloud
from urlextract import URLExtract
from emoji import demojize
import re
from collections import Counter

extract = URLExtract()

def fetch_stats(selected_user, df):
    """Fetch statistics for selected user or overall chat."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Number of messages
    num_messages = df.shape[0]
    
    # Number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    # Number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    
    # Number of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    
    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    """Get most active users in the chat."""
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).rename('Percentage')
    return x, new_df.head()


def create_wordcloud(selected_user, df):
    """Create word cloud for selected user or overall."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    
    # Filter out group notifications and media
    df_filtered = df[df['user'] != 'group_notification']
    df_filtered = df_filtered[df_filtered['message'] != '<Media omitted>']
    
    if len(df_filtered) > 0:
        wc.generate(' '.join(df_filtered['message'].values))
    
    return wc


def most_common_words(selected_user, df):
    """Get most common words used by selected user."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    
    # Common stop words
    stop_words = ['a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                  'could', 'can', 'may', 'might', 'must', 'shall', 'am', 'not', 'no',
                  'yes', 'you', 'i', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her']
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and len(word) > 2:
                words.append(word)
    
    most_common = Counter(words).most_common(20)
    return pd.DataFrame(most_common, columns=['word', 'frequency'])


def emoji_helper(selected_user, df):
    """Extract emojis used by selected user."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        data = demojize(message)
        emoji_pattern = r':[a-z_]+:'
        matches = re.findall(emoji_pattern, data)
        emojis.extend(matches)
    
    if not emojis:
        return pd.DataFrame(columns=['emoji', 'frequency'])
    
    emoji_count = Counter(emojis).most_common(20)
    return pd.DataFrame(emoji_count, columns=['emoji', 'frequency'])


def monthly_timeline(selected_user, df):
    """Get message count by month."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    if len(df) == 0:
        # Return empty dataframe with proper structure
        return pd.DataFrame(columns=['year', 'month_num', 'message', 'month_name', 'time'])
    
    # Group by year and month_num and count messages
    timeline = df.groupby(['year', 'month_num']).size().reset_index(name='message')
    
    # Convert month number to month name
    timeline['month_name'] = timeline['month_num'].apply(lambda x: pd.Timestamp(year=2024, month=int(x), day=1).strftime('%B'))
    
    # Create time column for display
    timeline['time'] = timeline['month_name'].astype(str) + '-' + timeline['year'].astype(str)
    
    # Sort by year and month
    timeline = timeline.sort_values(['year', 'month_num']).reset_index(drop=True)
    
    return timeline


def daily_timeline(selected_user, df):
    """Get message count by day."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').size().reset_index(name='message')
    return daily_timeline


def week_activity_map(selected_user, df):
    """Get activity by day of week."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    """Get activity by month."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    """Get activity heatmap data (day and hour)."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    if len(df) == 0:
        # Return empty dataframe
        return pd.DataFrame()
    
    try:
        # Create a copy and add a counter column for counting
        df_copy = df.copy()
        df_copy['count'] = 1
        
        # Create pivot table with count
        user_heatmap = df_copy.pivot_table(index='day_name', columns='hour', values='count', aggfunc='sum')
        
        # Fill NaN values with 0
        user_heatmap = user_heatmap.fillna(0).astype(int)
        
        # Ensure all hours 0-23 exist
        for hour in range(24):
            if hour not in user_heatmap.columns:
                user_heatmap[hour] = 0
        
        # Sort columns by hour
        user_heatmap = user_heatmap.sort_index(axis=1)
        
        # Reorder days correctly
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        existing_days = [day for day in day_order if day in user_heatmap.index]
        
        if len(existing_days) > 0:
            user_heatmap = user_heatmap.reindex(existing_days)
        else:
            return pd.DataFrame()
        
        return user_heatmap
    except Exception as e:
        print(f"Heatmap error: {str(e)}")
        return pd.DataFrame()










