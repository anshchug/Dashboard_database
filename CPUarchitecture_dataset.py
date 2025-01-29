import pandas as pd
import h5py
import numpy as np

# Function to read the CSV file and search for the subgroup name
def extract_value_from_csv(csv_file, column_name, subgroup_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Search for the subgroup name in the specified column
    matching_row = df[df[column_name].str.contains(subgroup_name, case=False, na=False)]

    columns_to_extract = [1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 14, 15, 16, 17, 18]
    value_column = list(df.columns[columns_to_extract])
    #print("Selected Headers:", value_column)
    extracted_value = np.array([])
    # If a match is found, return the value from the desired column
    if not matching_row.empty:
        # Assuming you want to extract data from another column (e.g., 'ValueColumn')
        #value_column = 'Max. Boost Clock'  # Replace with the actual column name from which you want to extract data
        for column in value_column:
            extracted_value = np.append(extracted_value, matching_row.iloc[0][column])
    else:
        print(f"No match found for subgroup '{subgroup_name}' in the CSV file.")
        value_column = None
        extracted_value = None
    return value_column, extracted_value
    
        

# Function to add the extracted value to the HDF5 file
def add_data_to_hdf5(h5_file, group_name, subgroup_name, value_column, data):
    group = h5_file[group_name]
    if subgroup_name not in group:
        print(f"While writing to the file, subgroup {subgroup_name} not found in the group {group_name}")
        pass
    else:
        subgroup = group[subgroup_name]
        
    # Create a dataset within the subgroup and store the extracted data
    value_encoded = np.array([s.encode('utf-8') for s in value_column], dtype='S')
    data_encoded = np.array([s.encode('utf-8') for s in data], dtype='S')
    #print(value_encoded, type(value_encoded))
    #print(data_encoded, type(data_encoded))
    combined_data = np.column_stack((value_encoded, data_encoded))
    #print(combined_data, type(combined_data))
    print(f"Creating dataset for CPU:{subgroup_name}")
    subgroup.create_dataset('CPU_architecture', data=combined_data)
    print(f"Data added to subgroup '{subgroup_name}' in group '{group_name}'.\n \t--------------------------------------------\n")

# Main process
def process_hdf5_and_csv(h5_file, csv_file, csv_column_name):
    with h5py.File(h5_file, 'r+') as f:
        # Iterate over all the groups in the HDF5 file
        for group_name in f:
            count = 0
            group = f[group_name]
            
            # Iterate over all subgroups within the current group
            for subgroup_name in group:
                count += 1
                # Extract the value from the CSV file using the subgroup name
                
                value_column, extracted_value = extract_value_from_csv(csv_file, csv_column_name, subgroup_name)
                if count == 1:
                    print(f"The following categories are extracted for CPU, {subgroup_name}:\n {value_column}")
                print(f"The corresponding values of the categories for CPU, {subgroup_name} are:\n{extracted_value}\n")

                subgroup = group[subgroup_name]
                if 'CPU_architecture' in subgroup:
                    del subgroup['CPU_architecture']
                if extracted_value is not None:
                    # Add the extracted value to the HDF5 file
                    add_data_to_hdf5(f, group_name, subgroup_name, value_column, extracted_value)
                else:
                    print(f"Subgroup '{subgroup_name}' not found in the CSV file.")
            print(f"Group {group_name} has {count} subgroups.")

# Example Usage
h5_file = 'dashboard_database.h5'  # Replace with the path to your HDF5 file
csv_file = 'Server Processor Specifications.csv'  # Replace with the path to your CSV file
csv_column_name = 'Name'  # Replace with the column name where subgroup names are stored

# Call the main function
process_hdf5_and_csv(h5_file, csv_file, csv_column_name)
