import requests
import h5py
import numpy as np

# API URL
#url = "http://stagingdashboard.amd.com/avg/result/9684X/wrf/latest"
#url = "http://stagingdashboard.amd.com/avg/result/9654/wrf/latest"
url_cpulist = "http://stagingdashboard.amd.com/cpusByCategory?categories=hpc"
header_cpulist = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://stagingdashboard.amd.com/perfAndScaling",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Cookie": "_mkto_trk=id:885-ZYT-361&token:_mch-amd.com-1722599728020-30604; __de_uid=4-c7cdr35g-lzcneh8u; _ga=GA1.1.1708146945.1722599729; _fbp=fb.1.1722599730073.186273342749181019; _cc_id=d7204cc2449d27813b2f3e5b0bc33525; coveo_visitorId=f6e18121-4f4a-4c32-bb8a-267418508966; _gcl_au=1.1.297574871.1733389878; panoramaId_expiry=1738211517314; panoramaId=db5cd2e5e71c04876f38aaee015d4945a7028cbc2ce7d147b270093ae4f3aab5; panoramaIdType=panoIndiv; _clck=dnph7p%7C2%7Cfsy%7C1%7C1675; ak_bmsc=DD7C7461AB4769AD0BFBAE47FC2FBA8A~000000000000000000000000000000~YAAQBmfRF/yfXJWUAQAAGd4eqxpZ0A25mmwOl7uJqYeDArmZmziVdKmf1Pwu3WA2P5z4y7GnAqVhl9sm859xRKb5sXu6HsJfWXKgGB5hM4WqLjP4lDSxbFBGniYb0w2IxTO+fKV/PVrYgmuzycxnN7y1kXLRbVDWV4Sn4DYyxc0sVvdPL2LTebsRNinTCEVWlJ++KkroBQAel8CPzHNz3gl8DFk9Bi8g64xCCP98KQcmKRpFihgc9PDw1sdFBEHYtfkmYIoMMJQwPLIQTAiDsK5chFowZEh3kB5EUJnK/Kk6KTzxr1Ps6mR1KmyN5f9oAil1IPjqbrueFnBZ41Jf5QzuinMrB3VXiy9A1LujPxXBDPgpPMryKSy/XYW0FRfSgZV0ka0mAbCx; bm_sz=64336CF87A5C36A4733B39694C21AFDD~YAAQBmfRF0yiXJWUAQAAP/MeqxopiN1VJ/G7nLQuIvQNF4Qm+PASCv2ktCx9NN/aBx6DafShLuLHuScLgPeNptej2gsvrMOoMPHPWBB0f+RHufbkoxye/6ByIxwkAskPUrG7JSCC44Kt36O+X7yTmJRpOEsewzxxW+3Qeohfb0ZMsDCexzkXCAM2KFvAGlxRz6uwUcbX1t0yQ/45gftGPtSSE3JCQ0UAa2Isv6kslxnNllu4tQs8l1bUDwUDNRChA3htH2VUl51R2rHkXdaJctd8b8P80uonJ8sskMPQJsBAK6ev8lucYXrH2C+a0Jm1RxDOZHlow2rDF6zzF0wXhncn1splQRXauep8iEPYzGOKXQbd0OkzDiiH+U3i06UgePDaTza9TYDzhe3gjd6eskaX~3684418~4468793; JSESSIONID=A21B7B2DF36FBB992E8D317F5AA6CC97; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jan+28+2025+10%3A28%3A00+GMT%2B0530+(India+Standard+Time)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=7cbc60b3-7787-4f7e-b9c7-00973edfee3c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0004%3A1%2CC0003%3A1%2CC0001%3A1&intType=1&geolocation=IN%3BMH&AwaitingReconsent=false; OptanonAlertBoxClosed=2025-01-28T04:58:00.035Z; _ga_KH6HWYNV1D=GS1.1.1738039695.59.1.1738040285.59.0.433075497; _ga_L205D9TRLT=GS1.1.1738039695.5.1.1738040285.59.0.0;"
}

try:
    # Sending GET request
    # response = requests.get(url, headers= header)
    response = requests.get(url_cpulist, headers=header_cpulist)

    # Check if the request was successful
    if response.status_code == 200:
        print("Fetching list of available CPUs!")
        cpu_list = response.json()  # Assuming the response is in JSON format
        with h5py.File('dashboard_database.h5', 'w') as file:
            pass
        for key, value in cpu_list.items():
            print(f"Key: {key}, Value: {value}")
            print(key, type(key))
            with h5py.File('dashboard_database.h5', 'a') as file:
                group = file.create_group(key)
                count = 0
                string_dtype = h5py.string_dtype(encoding='utf-8')
                for i in range(len(value)):
                    print(value[i], type(value[i]))
                    if group:
                        subgroup = group.create_group(value[i])
                    else:
                        print(f"Group {key} was not created properly")
                    print(value[i])
                    url_applist = "http://stagingdashboard.amd.com/appsByTypeCategory?cpu=" + value[i] + "&type=latest&category%5B%5D=hpc&ajax=true"
                    if key == 'Turin':
                        url_applist = "http://stagingdashboard.amd.com/appsByTypeCategory?cpu=" + value[i] + "&type=turin_launch&category%5B%5D=hpc&ajax=true"
                    #print(url_applist)
                    header_applist = {
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Connection": "keep-alive",
                        "X-Requested-With": "XMLHttpRequest",
                        "Referer": "http://stagingdashboard.amd.com/perfAndScaling",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                        "Cookie": "_mkto_trk=id:885-ZYT-361&token:_mch-amd.com-1722599728020-30604; __de_uid=4-c7cdr35g-lzcneh8u; _ga=GA1.1.1708146945.1722599729; _fbp=fb.1.1722599730073.186273342749181019; _cc_id=d7204cc2449d27813b2f3e5b0bc33525; coveo_visitorId=f6e18121-4f4a-4c32-bb8a-267418508966; _gcl_au=1.1.297574871.1733389878; panoramaId_expiry=1738211517314; panoramaId=db5cd2e5e71c04876f38aaee015d4945a7028cbc2ce7d147b270093ae4f3aab5; panoramaIdType=panoIndiv; _clck=dnph7p%7C2%7Cfsy%7C1%7C1675; ak_bmsc=DD7C7461AB4769AD0BFBAE47FC2FBA8A~000000000000000000000000000000~YAAQBmfRF/yfXJWUAQAAGd4eqxpZ0A25mmwOl7uJqYeDArmZmziVdKmf1Pwu3WA2P5z4y7GnAqVhl9sm859xRKb5sXu6HsJfWXKgGB5hM4WqLjP4lDSxbFBGniYb0w2IxTO+fKV/PVrYgmuzycxnN7y1kXLRbVDWV4Sn4DYyxc0sVvdPL2LTebsRNinTCEVWlJ++KkroBQAel8CPzHNz3gl8DFk9Bi8g64xCCP98KQcmKRpFihgc9PDw1sdFBEHYtfkmYIoMMJQwPLIQTAiDsK5chFowZEh3kB5EUJnK/Kk6KTzxr1Ps6mR1KmyN5f9oAil1IPjqbrueFnBZ41Jf5QzuinMrB3VXiy9A1LujPxXBDPgpPMryKSy/XYW0FRfSgZV0ka0mAbCx; bm_sz=64336CF87A5C36A4733B39694C21AFDD~YAAQBmfRF0yiXJWUAQAAP/MeqxopiN1VJ/G7nLQuIvQNF4Qm+PASCv2ktCx9NN/aBx6DafShLuLHuScLgPeNptej2gsvrMOoMPHPWBB0f+RHufbkoxye/6ByIxwkAskPUrG7JSCC44Kt36O+X7yTmJRpOEsewzxxW+3Qeohfb0ZMsDCexzkXCAM2KFvAGlxRz6uwUcbX1t0yQ/45gftGPtSSE3JCQ0UAa2Isv6kslxnNllu4tQs8l1bUDwUDNRChA3htH2VUl51R2rHkXdaJctd8b8P80uonJ8sskMPQJsBAK6ev8lucYXrH2C+a0Jm1RxDOZHlow2rDF6zzF0wXhncn1splQRXauep8iEPYzGOKXQbd0OkzDiiH+U3i06UgePDaTza9TYDzhe3gjd6eskaX~3684418~4468793; JSESSIONID=A21B7B2DF36FBB992E8D317F5AA6CC97; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jan+28+2025+10%3A28%3A00+GMT%2B0530+(India+Standard+Time)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=7cbc60b3-7787-4f7e-b9c7-00973edfee3c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0004%3A1%2CC0003%3A1%2CC0001%3A1&intType=1&geolocation=IN%3BMH&AwaitingReconsent=false; OptanonAlertBoxClosed=2025-01-28T04:58:00.035Z; _ga_KH6HWYNV1D=GS1.1.1738039695.59.1.1738040285.59.0.433075497; _ga_L205D9TRLT=GS1.1.1738039695.5.1.1738040285.59.0.0; _clsk=877jkq%7C1738040321112%7C2%7C0%7Ce.clarity.ms%2Fcollect"
                    }
                    applist_response = requests.get(url_applist, headers=header_applist)
                    if(applist_response.status_code == 200):
                        print(f"Fetching list of apps for cpu: {key}:{value[i]}")
                        app_list = applist_response.json()
                        if(len(app_list) == 0):
                            del file[f'/{key}/{value[i]}']
                            count += 1
                            print("empty app list")
                            pass
                        else:
                            for a in range(len(app_list)):
                                subgroup2 = subgroup.create_group(app_list[a])
                                print(app_list[a])
                                url_app = "http://stagingdashboard.amd.com/avg/result/" + value[i] + "/" + app_list[a] + "/latest"
                                if key == 'Turin':
                                    url_app = "http://stagingdashboard.amd.com/avg/result/" + value[i] + "/" + app_list[a] + "/turin_launch"
                                app_response = requests.get(url_app)
                                if(app_response.status_code == 200):
                                    app_data = app_response.json()
                                    columns = []
                                    indices = [1, 2, 3, 6, 7, 9, 10, 11, 14, 15]
                                    for idx in range(len(app_data)):
                                        print(app_data[idx], type(app_data[idx]))
                                        dict = app_data[idx]
                                        if idx == 0:
                                            key_arrays = np.array(list(dict.keys()), dtype='S')
                                            columns.append(key_arrays[indices])
                                            #subgroup2.create_dataset('Keys', data= key_arrays)
                                        value_arrays = np.array([str(value).encode('ascii', errors='ignore') for value in dict.values()], dtype='S')
                                        columns.append(value_arrays[indices])
                                        #subgroup2.create_dataset(f'Run_{idx+1}', data = value_arrays)
                                    combined_data = np.column_stack(columns)
                                    subgroup2.create_dataset('benchmarks_metrics', data=combined_data)
                                else:
                                    print("Fetching bechmark/app data failed with status code:", app_response.status_code)
                                    print("Response Text:", app_response.text)


                    else:
                        print(f"Fetching app list failed with status code: {applist_response.status_code}")
                        print("Response Text:", applist_response.text)
                    if count == len(value):
                        del file[f'/{key}']
                        print("All cpus have empty app list")
                
    else:
        print(f"Fetching cpulist failed with status code: {response.status_code}")
        print("Response Text:", response.text)
    


except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
