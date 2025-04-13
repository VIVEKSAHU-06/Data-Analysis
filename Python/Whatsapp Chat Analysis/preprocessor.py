import pandas as pd
import re
import datetime

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Replace the narrow no-break space with a regular space
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=False)

    # Conversion with error handling
    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
    except pd.errors.ParserError:
        print("Warning: Some dates might not be parsable in the expected format. Consider adjusting the format string or handling invalid dates.")
        #If date format is invalid, create empty columns to avoid further errors
        df['year'] = None
        df['month'] = None
        df['day'] = None
        df['hour'] = None
        df['minute'] = None
        return df #Return the dataframe at this point, so it doesnt try to access date properties further down

    user = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            user.append(entry[1])
            messages.append(" ".join(entry[2]))
        else:
            user.append('group_notification')
            messages.append(entry[0])

    df['user'] = user
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Now that we know message_date parsed correctly (because we're past the try/except), extract date parts
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['month_num']=df['message_date'].dt.month
    df['day'] = df['message_date'].dt.day
    df['only_date'] = df['message_date'].dt.date
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    
    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) +"-" + str("00"))
        elif hour == 0:
            period.append(str("00") +"-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    
    df['period'] = period

    return df
