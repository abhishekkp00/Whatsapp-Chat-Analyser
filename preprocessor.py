import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    """Preprocess WhatsApp chat data from exported text file."""
    
    # Try multiple regex patterns for different WhatsApp date formats
    patterns = [
        r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM|am|pm))\s-\s',  # 12-hour format with AM/PM
        r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{2}:\d{2})\s-\s',  # 24-hour format
        r'(\d{4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}:\d{2})\s',  # Alternative format
        r'(\d{1,2}-\d{1,2}-\d{2,4},\s\d{1,2}:\d{2})\s-\s',  # Another variant
    ]
    
    messages = []
    dates = []
    
    for pattern in patterns:
        try:
            dates = re.findall(pattern, data)
            if dates and len(dates) > 5:  # Found enough matches
                messages = re.split(pattern, data)[1:]
                # Remove empty strings
                messages = [m.strip() for m in messages if m.strip()]
                break
        except:
            continue
    
    if not dates or not messages:
        return pd.DataFrame()
    
    # Balance messages and dates
    if len(messages) > len(dates):
        messages = messages[:len(dates)]
    elif len(dates) > len(messages):
        dates = dates[:len(messages)]
    
    df = pd.DataFrame({'message_date': dates, 'user_message': messages})
    
    # Parse dates with multiple format attempts
    date_formats = [
        '%m/%d/%Y, %I:%M %p',  # MM/DD/YYYY, hh:mm AM/PM
        '%d/%m/%Y, %H:%M',      # DD/MM/YYYY, hh:mm
        '%m/%d/%y, %I:%M %p',   # M/D/YY, h:mm AM/PM
        '%d/%m/%y, %H:%M',      # D/M/YY, h:mm
    ]
    
    parsed_dates = None
    for fmt in date_formats:
        try:
            parsed_dates = pd.to_datetime(df['message_date'], format=fmt)
            break
        except:
            continue
    
    if parsed_dates is None:
        # Fallback to flexible parsing
        parsed_dates = pd.to_datetime(df['message_date'], errors='coerce')
    
    df['message_date'] = parsed_dates
    
    # Remove rows with invalid dates
    df = df[df['message_date'].notna()].reset_index(drop=True)
    
    if len(df) == 0:
        return pd.DataFrame()
    
    # Extract user and message
    users = []
    messages_list = []
    
    for message in df['user_message']:
        # Split by first colon followed by space
        entry = re.split(r':\s', message, 1)
        if len(entry) == 2:
            user = entry[0].strip()
            msg = entry[1].strip()
            # Check if user looks valid (not too long, no special patterns)
            if len(user) < 50 and not user.startswith('http'):
                users.append(user)
                messages_list.append(msg)
            else:
                users.append('group_notification')
                messages_list.append(message)
        else:
            users.append('group_notification')
            messages_list.append(message)
    
    df['user'] = users
    df['message'] = messages_list
    df.drop(columns=['user_message'], inplace=True)
    
    # Extract date components - with error handling
    try:
        df['only_date'] = df['message_date'].dt.date
        df['year'] = df['message_date'].dt.year
        df['month_num'] = df['message_date'].dt.month
        df['month'] = df['message_date'].dt.month_name()
        df['day'] = df['message_date'].dt.day
        df['day_name'] = df['message_date'].dt.day_name()
        df['hour'] = df['message_date'].dt.hour
        df['minute'] = df['message_date'].dt.minute
    except Exception as e:
        print(f"Error extracting date components: {str(e)}")
        return pd.DataFrame()
    
    return df
