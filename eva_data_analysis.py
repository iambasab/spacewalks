
import json
import datetime as dt
import csv
import matplotlib.pyplot as plt

# https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva-data.json', 'r', encoding='ascii')
output_file = open('./eva-data.csv','w', encoding='utf-8')
graph_file = 'cumulative_eva_graph.png'

# fieldnames = ("EVA #", "Country", "Crew", "Vehicle", "Date", "Duration", "Purpose")

data=[]


for i in range(375):
    line=input_file.readline()
    print(line)
    data.append(json.loads(line[1:-1]))
#data.pop(0)

## Comment out this bit if you don't want the spreadsheet
csv_writer=csv.writer(output_file)


time = []
date =[]

j=0
for i in data:
    print(data[j])
    # and this bit
    csv_writer.writerow(data[j].values())
    if 'duration' in data[j].keys():
        var_time_1=data[j]['duration']
        if var_time_1 == '':
            pass
        else:
            var_time_0=dt.datetime.strptime(var_time_1,'%H:%M')
            var_time_2 = dt.timedelta(hours=var_time_0.hour, minutes=var_time_0.minute, seconds=var_time_0.second).total_seconds()/(60*60)
            print(var_time_0,var_time_2)
            time.append(var_time_2)
            if 'date' in data[j].keys():
                date.append(dt.datetime.strptime(data[j]['date'][0:10], '%Y-%m-%d'))
                #date.append(data[j]['date'][0:10])

            else:
                time.pop(0)
    j+=1

var_time_0=[0]
for i in time:
    var_time_0.append(var_time_0[-1]+i)

date,time = zip(*sorted(zip(date, time)))



plt.plot(date,var_time_0[1:], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
