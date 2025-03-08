import re
import pandas as pd

def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s(?:am|pm)\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_messages':messages,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'],format='%d/%m/%y, %I:%M %p - ')
    df.rename(columns={'message_date':'date'},inplace=True)
    users=[]
    messages=[]
    for message in df['user_messages']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
          users.append(entry[1])
          messages.append(entry[2])
        else:
          users.append('group_notification')
          messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_messages'],inplace=True)
    df['month']=df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['year']=df['date'].dt.year
    df['only_date']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period = []
    for hour in df['hour']:
      if hour == 23:
        period.append(f"{hour}-00")
      elif hour == 0:
        period.append(f"00-{hour + 1:02d}")
      else:
       period.append(f"{hour:02d}-{hour + 1:02d}")

    df['period']=period

    return df