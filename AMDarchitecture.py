import pandas as pd
import h5py
import numpy as np

# Function to read the CSV file and search for the subgroup name
def extract_value_from_csv(csv_file, column_name, cpu_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Search for the cpu name in the specified column
    matching_row = df[df[column_name].str.contains(cpu_name, case=False, na=False)]

    columns_to_extract = [2, 3, 4, 6, 7, 9, 18]
    value_column = list(df.columns[columns_to_extract])
    extracted_value = np.array([])
    # If a match is found, return the value from the desired column
    if not matching_row.empty:
        for column in value_column:
            extracted_value = np.append(extracted_value, matching_row.iloc[0][column])
    else:
        print(f"No match found for cpu name '{cpu_name}' in the CSV file.")
        value_column = None
        extracted_value = None
    return value_column, extracted_value
    
        

#Function to add the extracted value to the HDF5 file
# def add_dataset_to_hdf5(h5_file, group_name, column_value, data):
#     group = h5_file[group_name]
#     # Create a dataset within the group and store the extracted data
#     for d in range(len(data)):

#     value_encoded = np.array([s.encode('utf-8') for s in value_column], dtype='S')
#     data_encoded = np.array([s.encode('utf-8') for s in data], dtype='S')
#     #print(value_encoded, type(value_encoded))
#     #print(data_encoded, type(data_encoded))
#     combined_data = np.column_stack((value_encoded, data_encoded))
#     #print(combined_data, type(combined_data))
#     print(f"Creating dataset for CPU:{subgroup_name}")
#     subgroup.create_dataset('CPU_architecture', data=combined_data)
#     print(f"Data added to subgroup '{subgroup_name}' in group '{group_name}'.\n \t--------------------------------------------\n")

# # Main process
# def process_hdf5_and_csv(h5_file, csv_file, csv_column_name):
#                 if count == 1:
#                     print(f"The following categories are extracted for CPU, {subgroup_name}:\n {value_column}")
#                 print(f"The corresponding values of the categories for CPU, {subgroup_name} are:\n{extracted_value}\n")

#                 subgroup = group[subgroup_name]
#                 if 'CPU_architecture' in subgroup:
#                     del subgroup['CPU_architecture']
#                 if extracted_value is not None:
#                     # Add the extracted value to the HDF5 file
#                     add_data_to_hdf5(f, group_name, subgroup_name, value_column, extracted_value)
#                 else:
#                     print(f"Subgroup '{subgroup_name}' not found in the CSV file.")
#             print(f"Group {group_name} has {count} subgroups.")
