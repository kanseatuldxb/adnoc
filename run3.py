



import pandas as pd
import difflib
sheet=pd.read_excel(open('Events.xlsx', 'rb'),sheet_name='Sheet1')
#print(sheet[['PlatesNo']].to_numpy())


print(difflib.get_close_matches('15958', ['K26958','15958']))

#https://youtu.be/lO9G36LZ6Bw

exit()

a = []
data = sheet[['PlatesNo']].to_numpy()
for i in data:
    print(i[0])
    a.append(str(i[0]))
a.append("1369618")
print(a)



for i in a:
    match = difflib.get_close_matches(i, a)
    print(i , " -> ", match)
    
    
import datetime
  
# datetime(year, month, day, hour, minute, second)
a = datetime.datetime(2017, 6, 21, 18, 25, 30)
b = datetime.datetime(2017, 5, 16, 8, 21, 10)
  
# returns a timedelta object
c = a-b 
print('Difference: ', c)
  
# returns (minutes, seconds)
minutes = divmod(c.total_seconds(), 60) 
print('Total difference in minutes: ', minutes[0], 'minutes',minutes[1], 'seconds')
  
# returns the difference of the time of the day (minutes, seconds)
minutes = divmod(c.seconds, 60) 
print('Total difference in minutes: ', minutes[0], 'minutes',minutes[1], 'seconds')
