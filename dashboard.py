import requests
import h5py
import numpy as np
import AMDarchitecture
import re
import add_intel_info

#API URL
url_cpulist = "http://stagingdashboard.amd.com/cpusByCategory?categories=hpc"
header_cpulist = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://stagingdashboard.amd.com/perfAndScaling",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Cookie": "_mkto_trk=id:885-ZYT-361&token:_mch-amd.com-1722599728020-30604; __de_uid=4-c7cdr35g-lzcneh8u; _ga=GA1.1.1708146945.1722599729; _fbp=fb.1.1722599730073.186273342749181019; _cc_id=d7204cc2449d27813b2f3e5b0bc33525; coveo_visitorId=f6e18121-4f4a-4c32-bb8a-267418508966; _gcl_au=1.1.297574871.1733389878; panoramaId_expiry=1738825824999; panoramaId=db5cd2e5e71c04876f38aaee015d4945a7028cbc2ce7d147b270093ae4f3aab5; panoramaIdType=panoIndiv; OptanonAlertBoxClosed=2025-01-31T04:56:58.580Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+31+2025+10%3A26%3A59+GMT%2B0530+(India+Standard+Time)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=7cbc60b3-7787-4f7e-b9c7-00973edfee3c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0004%3A1%2CC0003%3A1%2CC0001%3A1&intType=1&geolocation=IN%3BMH&AwaitingReconsent=false; _ga_KH6HWYNV1D=GS1.1.1738299419.66.0.1738299419.60.0.1343122428; _ga_L205D9TRLT=GS1.1.1738299419.12.0.1738299419.60.0.0; _clck=dnph7p%7C2%7Cft1%7C1%7C1675; JSESSIONID=0EB0E0B543EF6FBB846BC223608101C4"
}
header_applist = {
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Connection": "keep-alive",
                        "X-Requested-With": "XMLHttpRequest",
                        "Referer": "http://stagingdashboard.amd.com/perfAndScaling",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                        "Cookie": "_mkto_trk=id:885-ZYT-361&token:_mch-amd.com-1722599728020-30604; __de_uid=4-c7cdr35g-lzcneh8u; _ga=GA1.1.1708146945.1722599729; _fbp=fb.1.1722599730073.186273342749181019; _cc_id=d7204cc2449d27813b2f3e5b0bc33525; coveo_visitorId=f6e18121-4f4a-4c32-bb8a-267418508966; _gcl_au=1.1.297574871.1733389878; panoramaId_expiry=1738825824999; panoramaId=db5cd2e5e71c04876f38aaee015d4945a7028cbc2ce7d147b270093ae4f3aab5; panoramaIdType=panoIndiv; OptanonAlertBoxClosed=2025-01-31T04:56:58.580Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+31+2025+10%3A26%3A59+GMT%2B0530+(India+Standard+Time)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=7cbc60b3-7787-4f7e-b9c7-00973edfee3c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0004%3A1%2CC0003%3A1%2CC0001%3A1&intType=1&geolocation=IN%3BMH&AwaitingReconsent=false; _ga_KH6HWYNV1D=GS1.1.1738299419.66.0.1738299419.60.0.1343122428; _ga_L205D9TRLT=GS1.1.1738299419.12.0.1738299419.60.0.0; _clck=dnph7p%7C2%7Cft1%7C1%7C1675; JSESSIONID=0EB0E0B543EF6FBB846BC223608101C4"
                    }
AMD_cpus = ['Naples', 'Rome', 'Milan', 'Genoa', 'Turin']
Intel_cpus = ['Ice Lake', 'Sapphire Rapids', 'Emerald Rapids']
csv_file = 'Server Processor Specifications.csv'  # Replace with the path to your CSV file
csv_column_name = 'Name'
intel_arch = [{'8362' : {'Total Cores' : 32, 'Total Threads' : 64, 'Max Turbo Frequency (GHz)' : 3.60, 'Processor Base Frequency (GHz)' : 2.80, 'Cache (Mb)' : 48, 'Intel UPI Speed (GT/s)' : 11.2, 'Max # of UPI Links' : 3, 'TDP (W)': 265, 'Maximum Memory Speed (MHz)': 3200, 'Max # of Memory Channels': 8}}, 
              {'8380' : {'Total Cores' : 40, 'Total Threads' : 80, 'Max Turbo Frequency (GHz)' : 3.40, 'Processor Base Frequency (GHz)' : 2.30, 'Cache (Mb)' : 60, 'Intel UPI Speed (GT/s)' : 11.2, 'Max # of UPI Links' : 3, 'TDP (W)': 270, 'Maximum Memory Speed (MHz)': 3200, 'Max # of Memory Channels': 8}}, 
              {'8462Y' : {'Total Cores' : 32, 'Total Threads' : 64, 'Max Turbo Frequency (GHz)' : 4.10, 'Processor Base Frequency (GHz)' : 2.80, 'Cache (Mb)' : 60, 'Intel UPI Speed (GT/s)' : 16.0, 'Max # of UPI Links' : 3, 'TDP (W)': 300, 'Maximum Memory Speed (MHz)': 4800, 'Max # of Memory Channels': 8}}, 
              {'8490H' : {'Total Cores' : 60, 'Total Threads' : 120, 'Max Turbo Frequency (GHz)' : 3.50, 'Processor Base Frequency (GHz)' : 1.90, 'Cache (Mb)' : 112.5, 'Intel UPI Speed (GT/s)' : 16.0, 'Max # of UPI Links' : 4, 'TDP (W)': 350, 'Maximum Memory Speed (MHz)': 4800, 'Max # of Memory Channels': 8}}
            ]


def add_AMD_data(h5_file, g_name, b_name, app_name, perfMetric, cpu_values, dataset_names):
    print(f"Adding dataset for benchmark name {app_name.upper() + '_' + str(b_name)}")
    group = h5_file[g_name]
    group['b_name'].resize((group['b_name'].shape[0] + 1, ))
    group['b_name'][-1] = str(app_name.upper()) + '_' + str(b_name)
    group['perf_metric'].resize((group['perf_metric'].shape[0] + 1, ))
    group['perf_metric'][-1] = perfMetric
    group['L3_cache_per_core (MB)'].resize((group['L3_cache_per_core (MB)'].shape[0] + 1, ))
    group['L3_cache_per_core (MB)'][-1] = float(cpu_values[4]) /float(cpu_values[1])
    count = 0
    for name in dataset_names[3:]:
        group[name].resize((group[name].shape[0] + 1, ))
        group[name][-1] = cpu_values[count]
        count += 1



def add_app_data(app_list, h5_file, g_name, cpu_gen, cpu_name):
    if cpu_gen in AMD_cpus:
        dataset_names = ['b_name', 'perf_metric', 'L3_cache_per_core (MB)', 'cores', 'threads', 'max_freq (GHz)', 'base_freq (GHz)', 'L3 cache (MB)', 'TDP (W)', 'Mem_BW (GB per s)']
        names_type = [h5py.string_dtype(encoding='utf-8'), 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f']
    if cpu_gen in Intel_cpus:
        dataset_names = ['b_name', 'perf_metric', 'L3_cache_per_core (MB)', 'cores', 'threads', 'max_freq (GHz)', 'base_freq (GHz)', 'L3 cache (MB)', 'TDP (W)', 'Mem_Speed (MHz)', 'Mem channels']
        names_type = [h5py.string_dtype(encoding='utf-8'), 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f']
    
    count = 0
    for name in dataset_names:
        if name in h5_file[g_name]:
            del h5_file[g_name][name]
            #print(f"Deleting dataset {name}!")
        h5_file[g_name].create_dataset(name, shape=(0,), maxshape=(None,), chunks=True, dtype=names_type[count])
        count += 1
        #print(f"Dataset {name} created!")
    for a in range(len(app_list)):
        url_app = "http://stagingdashboard.amd.com/avg/result/" + cpu_name + "/" + app_list[a] + "/latest"
        if cpu_gen == 'Turin':
            url_app = "http://stagingdashboard.amd.com/avg/result/" + cpu_name + "/" + app_list[a] + "/turin_launch"
        app_response = requests.get(url_app)
        if (app_response.status_code == 200):
            app_data = app_response.json()
            for idx in range(len(app_data)):
                dict = app_data[idx]
                dict_values = list(dict.values())
                bname = dict_values[2]
                threads = dict_values[3]
                avgResult = dict_values[6]
                #print(f"For appname, '{app_list[a]}' and benchmark {bname} which runs on {cores} cores, the perf metric is {avgResult}")
                if cpu_gen in AMD_cpus:
                    column_value, extracted_value = AMDarchitecture.extract_value_from_csv(csv_file, csv_column_name, cpu_name)
                    extracted_value[2]= [float(word) for word in extracted_value[2].split() if word.replace('.', '', 1).isdigit()][0]
                    extracted_value[3]= [float(word) for word in extracted_value[3].split() if word.replace('.', '', 1).isdigit()][0]
                    extracted_value[4]= [float(word) for word in extracted_value[4].split() if word.replace('.', '', 1).isdigit()][0]
                    match = re.search(r"[-+]?\d*\.\d+|\d+", extracted_value[5])
                    if match:
                        extracted_value[5] = float(match.group())
                    #extracted_value[5]= [[float(word) for word in extracted_value[5].split() if word.isdigit()][0]]
                    extracted_value[6]= [float(word) for word in extracted_value[6].split() if word.replace('.', '', 1).isdigit()][0]
                    #print(f'column value: {column_value} and extracted value : {extracted_value} with type {type(extracted_value)}')
                    #print(float(extracted_value[1]))
                    if float(extracted_value[1]) == threads: # Only cases where the benchmark runs on the maximum number of cores are considered.
                        add_AMD_data(h5_file, g_name, bname, app_list[a], avgResult, extracted_value, dataset_names)
                    else:
                        print("Max no of cores do not match the no of cores utilized by benchmark (UNDER UTILIZATION OF THE CORES!)")
                        print(f"Max cores = {extracted_value[1]} whereas cores utilization = {threads}")

                if cpu_gen in Intel_cpus:
                    add_intel_info.extract_info(h5_file, g_name, bname, app_list[a], avgResult, threads, cpu_name, intel_arch, dataset_names)
        else:
            print("Error fetching app api!")
        print(f"Data added for all benchmarks in app {app_list[a]}!")


def create_dataset(h5_file, g_name):
    cpu_gen = g_name.split('-')[0]
    cpu_name = g_name.split('-')[-1]
    if cpu_gen != 'Turin':
        url_applist = "http://stagingdashboard.amd.com/appsByTypeCategory?cpu=" + cpu_name + "&type=latest&category%5B%5D=hpc&ajax=true"
    else:
        url_applist = "http://stagingdashboard.amd.com/appsByTypeCategory?cpu=" + cpu_name + "&type=turin_launch&category%5B%5D=hpc&ajax=true"
    applist_response = requests.get(url_applist, headers=header_applist)
    if applist_response.status_code == 200:
        print(f"Fetching list of apps for cpu: {g_name}")
        app_list = applist_response.json()
        if (len(app_list) == 0):
            del h5_file[g_name]
            print(f"Empty list of apps, hence deleting group, {g_name}")
        else:
            add_app_data(app_list, h5_file, g_name, cpu_gen, cpu_name)
            pass
    else:
        print('Error occured while fetching applist api!')     


def create_database(h5_file, cpu_list):
    for key, value in cpu_list.items():
        for i in range(len(value)):
            group_name = str(key) + '-' + str(value[i])
            if group_name in h5_file:
                print(f"Group {group_name} already exists!")
            else:
                h5_file.create_group(group_name)
                print(f"Group {group_name} created!")
            create_dataset(h5_file, group_name)

try:
    response = requests.get(url_cpulist, headers=header_cpulist)
    if response.status_code == 200:
        print("Fetching list of available CPUs:")
        cpu_list = response.json()
        with h5py.File('dashboard_database.h5', 'a') as file:
            create_database(file, cpu_list)
            print('Database created!\n')           
except requests.exceptions.RequestException as e:
    print(f"An error occured: {e}")