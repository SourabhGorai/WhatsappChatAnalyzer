import re
import pandas as pd


def preprocess(data):
    # Define the pattern for WhatsApp timestamps
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\s?-\s'

    # Split messages and extract dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime, handling 12-hour format with AM/PM
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')

    # Rename columns
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Split user and message content
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # If there is a user name
            users.append(entry[1])  # Extract the user name
            messages.append(" ".join(entry[2:]))  # Extract the message
        else:
            users.append('group_notification')
            messages.append(entry[0])

    # Add user and message columns
    df['user'] = users
    df['message'] = messages

    # Drop the original user_message column
    df.drop(columns=['user_message'], inplace=True)

    # Display the first few rows of the DataFrame
    # print(df.head())


    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df