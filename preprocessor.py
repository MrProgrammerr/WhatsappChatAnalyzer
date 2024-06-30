# import re
# import pandas as pd
# def preprocess(data):
#     pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)
#     df = pd.DataFrame({'User_Message': messages, 'Date': dates})
#     df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y, %H:%M - ')
#     users = []
#     messages = []
#     for msg in df['User_Message']:
#         splitted = re.split('([\w\W]+?):\s', msg)
#         if (len(splitted) == 1):
#             users.append('notification')
#             messages.append(splitted[0])
#         else:
#             users.append(splitted[1])
#             messages.append(splitted[2])
#     df['User'] = users
#     df['Message'] = messages
#     df.drop(['User_Message'], axis=1, inplace=True)
#     df['Year'] = df['Date'].dt.year
#     df['Month'] = df['Date'].dt.month_name()
#     df['Month_Num'] = df['Month'].map({'January': 1,'February': 2,'March': 3,'April': 4,'May': 5,'June': 6,'July': 7,'August': 8,'September': 9,'October': 10,'November': 11,'December': 12})
#     df['Day'] = df['Date'].dt.day
#     df['Day_Name'] = df['Date'].dt.day_name()
#     df['Hour'] = df['Date'].dt.hour
#     df['Minute'] = df['Date'].dt.minute

#     period = []
#     for hour in df['Hour']:
#         if hour == 23:
#             period.append(str(hour) + "-" + str('00'))
#         elif hour == 0:
#             period.append(str('00') + "-" + str(hour + 1))
#         else:
#             period.append(str(hour) + "-" + str(hour + 1))

#     df['Period'] = period
#     return df

import re
import pandas as pd

def preprocess(data):
    # Adjusted pattern to handle both 12-hour and 24-hour time formats
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[apmAPM]*\s*-\s'
    
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    # Determine the correct date format based on presence of AM/PM
    if re.search(r'[apmAPM]', dates[0]):
        date_format = '%d/%m/%y, %I:%M %p - '
    else:
        date_format = '%d/%m/%Y, %H:%M - '
    
    df = pd.DataFrame({'User_Message': messages, 'Date': dates})
    df['Date'] = pd.to_datetime(df['Date'], format=date_format)
    
    users = []
    messages = []
    for msg in df['User_Message']:
        splitted = re.split(r'([\w\W]+?):\s', msg)
        if len(splitted) == 1:
            users.append('notification')
            messages.append(splitted[0])
        else:
            users.append(splitted[1])
            messages.append(splitted[2])
    
    df['User'] = users
    df['Message'] = messages
    df.drop(['User_Message'], axis=1, inplace=True)
    
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Month_Num'] = df['Month'].map({
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    })
    df['Day'] = df['Date'].dt.day
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    
    period = []
    for hour in df['Hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-1")
        else:
            period.append(f"{hour}-{hour + 1}")
    
    df['Period'] = period
    return df

