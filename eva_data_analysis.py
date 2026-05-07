
import matplotlib.pyplot as plt
import pandas as pd
import sys
import re

def main(input_file, output_file, graph_file):
    print("--START--")

    # Read the data from JSON file
    eva_data = read_json_to_dataframe(input_file)

    # Calculate and add crew size to data
    eva_data = add_crew_size_column(eva_data) # added this line

    # Convert and export data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    # Sort dataframe by date ready to be plotted (date values are on x-axis)
    eva_data.sort_values('date', inplace=True)

    # Plot cumulative time spent in space over years
    plot_cumulative_time_in_space(eva_data, graph_file)

    print("--END--")


def read_json_to_dataframe(input_file):
    '''
    Read the data ffrom a JSON file to a pandas dataframe.
    Clean the data by removing any rows where duration is missing

    Args:
        input_file(file or string): the file object or the path to the JSON file

    Returns:
        eva_df(pd.DataFrame):nThe cleaned data as a dataframe st

    '''
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
    '''
    Save the dataframe to a CSV file

    Args:
        df(pd.DataFrame): The dataframe object that is to be saved as csv file
        output_file(file or string): the file object or the path to where the CSV file will be saved
    
    Returns:
        None
    '''

    print(f'Saving to CSV file {output_file}')
    # save the data to a csv file for later analysis
    df.to_csv(output_file, index=False, encoding='utf-8')


def plot_cumulative_time_in_space(df, graph_file):
    '''
    Plot the processed data

    Args:
        df(pd.DataFrame): The dataframe that is to be plotted 
        graph_file(file or string): The path to where the plot is to be saved as a .png file

    Returns:
        None
    
    '''
    print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')

    df=add_duration_hours(df)
    df['cumulative_time'] = df['duration_hours'].cumsum()

    ''' Visualise the output'''
    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()

def text_to_duration(duration):
    """
    Convert a text format duration "HH:MM" to duration in hours

    Args:
        duration (str): The text format duration

    Returns:
        duration_hours (float): The duration in hours
    """
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/60  # there is an intentional bug on this line (should divide by 60 not 6)
    return duration_hours

def add_duration_hours(df):
    """
    Add duration in hours (duration_hours) variable to the dataset

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        df_copy (pd.DataFrame): A copy of df with the new duration_hours variable added
    """
    df_copy = df.copy()
    df_copy["duration_hours"] = df_copy["duration"].apply(
        text_to_duration
    )
    return df_copy

def calculate_crew_size(crew):
    """
    Calculate the size of the crew for a single crew entry

    Args:
        crew (str): The text entry in the crew column containing a list of crew member names

    Returns:
        (int): The crew size
    """
    if crew.split() == []:
        return None
    else:
        return len(re.split(r';', crew))-1
    
def add_crew_size_column(df):
    """
    Add crew_size column to the dataset containing the value of the crew size

    Args:
        df (pd.DataFrame): The input data frame.

    Returns:
        df_copy (pd.DataFrame): A copy of the dataframe df with the new crew_size variable added
    """
    print('Adding crew size variable (crew_size) to dataset')
    df_copy = df.copy()
    df_copy["crew_size"] = df_copy["crew"].apply(
        calculate_crew_size
    )
    return df_copy

# Main code


# Data source: https://data.nasa.gov/resource/eva.json (with modifications)

'''# remember to add the encoding even if your machine doesn't give a problem now
# for input file the encoding is ascii for json, for output files, the encoding is utf-8 for csv'''

if __name__ == "__main__":
    datapath='./data/'
    if len(sys.argv) < 3:
        input_file = open(datapath+'eva-data.json', 'r', encoding='ascii') # input the json file
        output_file = open(datapath+'eva-data.csv', 'w', encoding='utf-8') # output file is in csv format
        print('Using default input and output filenames')
    else:
        input_file=datapath+sys.argv[1]
        output_file=datapath+sys.argv[2]
        print('Using custom input and output filenames')

    resultpath='./results/'
    graph_file = resultpath + 'cumulative_eva_graph.png' # name the file where the generated figure will be saved
    main(input_file, output_file, graph_file)