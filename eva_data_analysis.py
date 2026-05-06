
import matplotlib.pyplot as plt
import pandas as pd

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)

'''# remember to add the encoding even if your machine doesn't give a problem now
# for input file the encoding is ascii for json, for output files, the encoding is utf-8 for csv'''

input_file = open('./eva-data.json', 'r', encoding='ascii') # input the json file
output_file = open('./eva-data.csv', 'w', encoding='utf-8') # output file is in csv format

# name the file where the generated figure will be saved
graph_file = './cumulative_eva_graph.png' 

# We now use pandas to read the input file and once again specify the encoding format as ascii
eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii') 
eva_df['eva'] = eva_df['eva'].astype(float)
eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)

eva_df.to_csv(output_file, index=False, encoding='utf-8')

eva_df.sort_values('date', inplace=True) # data sorted along dates

eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()

''' Visualise the output'''
plt.plot(eva_df['date'], eva_df['cumulative_time'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
