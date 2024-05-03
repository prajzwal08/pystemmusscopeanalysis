"""
Script to copy the latest NetCDF file from each station's model output folder to a common output path.

Purpose:
This script iterates through a pandas DataFrame containing station information. For each station,
it checks if the model output folder exists, finds the latest folder within it, and copies the
latest NetCDF file from that folder to a specified output path.

Date: [3 May 2024, Friday]

Author: [Prajwal Khanal]

Environment:
- Python 3.x
- pandas
- shutil

Inputs:
- pystemmus_output_model_path: Path to the root folder containing model output folders for each station.
- file_path_station_info: Path to the CSV file containing station information.
- output_path: Path to the output folder where NetCDF files will be copied.

Outputs:
- Copies of the latest NetCDF files from each station's model output folder to the output_path.

"""

import os
import pandas as pd
import shutil

# Path to the root folder containing model output folders for each station
pystemmus_output_model_path = "/home/khanalp/STEMMUSSCOPE/STEMMUS_SCOPE/ICOS_sites/"

# Path to the CSV file containing station information
file_path_station_info = "/home/khanalp/code/PhD/preprocessICOSdata/output/csvs/stations_readyformodelrun.csv"

# Path to the output folder where NetCDF files will be copied
output_path = "/home/khanalp/data/processed/output_pystemmus"

# Read station information from CSV file into a pandas DataFrame
station_info = pd.read_csv(file_path_station_info, index_col=0)

# Iterate through each station in the DataFrame
for index, row in station_info.iterrows():
    station = row['Station_Name']
    print("Processing station:", station)
    
    # Construct the path to the model output folder for the current station
    modeloutput_folder_path = os.path.join(pystemmus_output_model_path, station, "output")
    
    # Check if the model output folder exists
    if os.path.exists(modeloutput_folder_path):
        # Get the latest folder created within the model output folder
        latest_folder = max((entry.path for entry in os.scandir(modeloutput_folder_path) if entry.is_dir()), key=os.path.getmtime)
        
        # Filter out NetCDF files within the latest folder
        nc_files = [file for file in os.listdir(latest_folder) if file.endswith('.nc')]
        
        # Check if NetCDF files exist
        if nc_files:
            # Construct the path to the latest NetCDF file
            nc_file_path = os.path.join(latest_folder, nc_files[0])
            
            # Copy the latest NetCDF file to the output path
            shutil.copy(nc_file_path, output_path)
        else:
            print("No NetCDF files found in", latest_folder)
    else:
        print("Model output folder does not exist for station:", station)
