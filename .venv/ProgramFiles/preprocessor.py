import pandas as pd
import re

def preprocess(data):
    data = data.replace('\u202f', ' ')
    pattern = r'(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?[ap]m) - (.*?)\n'

    # Separate arrays to store date-time and messages
    date_time_list = []
    messages_list = []

    # Extract all matches and append to respective lists
    matches = re.findall(pattern, data)
    for date_time, message in matches:
        date_time_list.append(date_time)
        messages_list.append(message)

    # Display the lists (optional)
    print("Date-Time List:", date_time_list)
    print("Messages List:", messages_list)

    dataset = pd.DataFrame({'date and time': date_time_list, 'message': messages_list})
    user = []
    messages = []

    # Assuming 'dataset' is a pandas DataFrame with the 'message' column containing the chat data
    for message in dataset['message']:
        # Applying the regex to split the message into user and content
        match = re.match(r"^(.*?):\s*(.*)", message)

        if match:
            user.append(match.group(1))  # Extracts the user (name or number)
            messages.append(match.group(2))  # Extracts the message
        else:
            user.append('Group Notification')  # In case of non-standard messages like system notifications
            messages.append(message)

    dataset['User'] = user
    dataset['Message'] = messages
    dataset['date and time'] = pd.to_datetime(dataset['date and time'], errors='coerce')
    dataset['Year'] = dataset['date and time'].dt.year
    dataset['Month'] = dataset['date and time'].dt.month_name()
    dataset['Day'] = dataset['date and time'].dt.day
    dataset['Hour'] = dataset['date and time'].dt.hour
    dataset['Minute'] = dataset['date and time'].dt.minute
    return dataset
