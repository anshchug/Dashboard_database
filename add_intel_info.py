import h5py
import numpy as np
import math

arch_info_url1 = 'https://www.intel.com/content/www/us/en/ark/products/codename/74979/products-formerly-ice-lake.html'


filename = 'dashboard_database.h5'

def extract_info(h5_file, g_name, bname, app_name, perfMetric, threads, cpu_name, intel_arch, dataset_names):
    flattened_intel_arch = {list(d.keys())[0]: list(d.values())[0] for d in intel_arch}
    value = flattened_intel_arch.get(cpu_name, None)
    intel_threads = (list(value.values())[1])
    cores = list(value.values())[0]
    max_freq = list(value.values())[2]
    base_freq = list(value.values())[3]
    L3_cache = list(value.values())[4]
    tdp = list(value.values())[7]
    mem_speed = list(value.values())[8]
    mem_channels = list(value.values())[9]
    mem_bw = round(mem_speed * mem_channels * 8 / (8 *1024)) #multipled by 8 as 64 bit (8 bytes) data bus is assumed and divided by 1024 to convert to Gb/s
    value_list = [cores, intel_threads, max_freq, base_freq, L3_cache, tdp, mem_speed, mem_channels]
    if (threads == intel_threads):    
        group = h5_file[g_name]
        group['b_name'].resize((group['b_name'].shape[0] + 1, ))
        group['b_name'][-1] = str(app_name.upper()) + '_' + str(bname)
        group['perf_metric'].resize((group['perf_metric'].shape[0] + 1, ))
        group['perf_metric'][-1] = perfMetric
        group['L3_cache_per_core (MB)'].resize((group['L3_cache_per_core (MB)'].shape[0] + 1, ))
        group['L3_cache_per_core (MB)'][-1] = L3_cache / cores

        count = 0
        for name in dataset_names[3:]:
            group[name].resize((group[name].shape[0] + 1, ))
            group[name][-1] = value_list[count]
            count += 1
    else:
        print("Max no of cores do not match the no of cores utilized by benchmark (UNDER UTILIZATION OF THE CORES!)")
        print(f"Max cores = {max_cores} whereas cores utilization = {threads}")
