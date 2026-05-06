
import matplotlib.pyplot as plt
import pandas as pd

def read_json_to_dataframe(input_file):
    print(f'Reading JSON file {input_file}')

    # We now use pandas to read the input file and once again specify the encoding format as ascii
    # EVA stands for extra vehicular activity
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii') 
    eva_df['eva'] = eva_df['eva'].astype(float)
    print(f'this is the pandas data variable where the input file is read into eva_df of size: {len(eva_df)}')

    # Clean the data by removing any rows where duration is missing
    eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)
    return eva_df


def write_dataframe_to_csv(df,output_file):
    print(f'Saving to CSV file {output_file}')
    # save the data to a csv file for later analysis
    df.to_csv(output_file, index=False, encoding='utf-8')

def plot_cumulative_time_in_space(df, graph_file):
    eva_data['duration_hours'] = eva_data['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
    eva_data['cumulative_time'] = eva_data['duration_hours'].cumsum()

    ''' Visualise the output'''
    plt.plot(eva_data['date'], eva_data['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()


# Main code
print("--START--")

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)

'''# remember to add the encoding even if your machine doesn't give a problem now
# for input file the encoding is ascii for json, for output files, the encoding is utf-8 for csv'''

input_file = open('./eva-data.json', 'r', encoding='ascii') # input the json file
output_file = open('./eva-data.csv', 'w', encoding='utf-8') # output file is in csv format

# name the file where the generated figure will be saved
graph_file = './cumulative_eva_graph.png' 



#read data from json file
eva_data=read_json_to_dataframe(input_file)

# Convert dataframe to csv file
write_dataframe_to_csv(eva_data,output_file)

# sort the dataframe ready to be plotted with data values on the x axis
eva_data.sort_values('date', inplace=True) 

# Plot cumulative time spent in space over the years
print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
plot_cumulative_time_in_space(eva_data,graph_file)


print("--END--")