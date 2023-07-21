from datetime import datetime

timedelta = '10.05.2023,14.05.2023'

str = timedelta.split(',')
l = []
print(datetime.strptime(str[0], "%d.%m.%Y"))
print(str[0])
# for i in str:
#     t = datetime.strptime(str[i], "%Y-%m-%d")
#     l.append(t)

print(str)