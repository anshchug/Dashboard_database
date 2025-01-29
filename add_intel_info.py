import h5py
import numpy as np

arch_info_url1 = 'https://www.intel.com/content/www/us/en/ark/products/codename/74979/products-formerly-ice-lake.html'

intel_arch = [{'8362' : {'Total Cores' : '32', 'Total Threads' : '64', 'Max Turbo Frequency' : '3.60 GHz', 'Processor Base Frequency' : '2.80 GHz', 'Cache' : '48 Mb', 'Intel UPI Speed' : '11.2 GT/s', 'Max # of UPI Links' : '3', 'TDP': '265 W', 'Maximum Memory Speed': '3200 MHz', 'Max # of Memory Channels': '8'}}, 
              {'8380' : {'Total Cores' : '40', 'Total Threads' : '80', 'Max Turbo Frequency' : '3.40 GHz', 'Processor Base Frequency' : '2.30 GHz', 'Cache' : '60 Mb', 'Intel UPI Speed' : '11.2 GT/s', 'Max # of UPI Links' : '3', 'TDP': '270 W', 'Maximum Memory Speed': '3200 MHz', 'Max # of Memory Channels': '8'}}, 
              {'8462Y' : {'Total Cores' : '32', 'Total Threads' : '64', 'Max Turbo Frequency' : '4.10 GHz', 'Processor Base Frequency' : '2.80 GHz', 'Cache' : '60 Mb', 'Intel UPI Speed' : '16.0 GT/s', 'Max # of UPI Links' : '3', 'TDP': '300 W', 'Maximum Memory Speed': '4800 MHz', 'Max # of Memory Channels': '8'}}, 
              {'8490H' : {'Total Cores' : '60', 'Total Threads' : '120', 'Max Turbo Frequency' : '3.50 GHz', 'Processor Base Frequency' : '1.90 GHz', 'Cache' : '112.5 Mb', 'Intel UPI Speed' : '16.0 GT/s', 'Max # of UPI Links' : '4', 'TDP': '350 W', 'Maximum Memory Speed': '4800 MHz', 'Max # of Memory Channels': '8'}}
            ]
filename = 'dashboard_database.h5'

def extract_info(h5_file, key, value):
    with h5py.File(h5_file, 'r+') as f:
        for group_name in f:
            group = f[group_name]
            for subgroup_name in group:
                if subgroup_name == key:
                    print(f"subgroup {subgroup_name} matched with key {key}")
                    subgroup = group[subgroup_name]
                    keys_array = np.array([key.encode('utf-8') for key in value.keys()], dtype='S')
                    values_array = np.array([key.encode('utf-8') for key in value.values()], dtype='S')
                    combined_data = np.column_stack((keys_array, values_array))
                    subgroup.create_dataset('CPU_architectire', data=combined_data)
                    #print(combined_data)
                    break
    f.close()

for i in range(len(intel_arch)):
    for key, value in intel_arch[i].items():
        print(f"Key: {key}")
        extract_info(filename, key, value)
