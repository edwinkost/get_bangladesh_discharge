#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

main_input_folder = "/scratch-shared/edwinhs/daily_discharge_aqueduct_flood_analyzer/m17/"

rcp_codes = ["2p6", "4p5", "6p0", "8p5", "historical_baseline"]
rcp_codes = ["2p6"]

#~ gcm_names       = ["GFDL-ESM2M", "HadGEM2-ES", "IPSL-CM5A-LR", "MIROC-ESM-CHEM", "NorESM1-M"]
#~ gcm_names       = ["GFDL-ESM2M"]
gcm_small_names    = ["gfdl-esm2m", "hadgem2-es", "ipsl-cm5a-lr", "miroc-esm-chem", "noresm1-m"]
gcm_small_names    = ["gfdl-esm2m"]


# station ids and coordinates 
     #~ 89.0417     26.2083    1
     #~ 89.7083     26.0417    2
      #~ 89.625      25.875    3
      #~ 89.875      25.875    4
     #~ 88.7083     25.7917    5
     #~ 89.4583     25.7917    6
     #~ 89.0417     25.7083    7
     #~ 89.7083      25.125    8
     #~ 88.7917     24.9583    9
     #~ 92.5417      24.875   10
      #~ 91.125     24.7083   11
     #~ 91.7083      24.625   12
     #~ 88.2083     24.4583   13
     #~ 91.2083      24.375   14
      #~ 89.625      24.125   15
     #~ 89.0417     24.0417   16
     #~ 90.9583     24.0417   17
     #~ 91.2083      23.875   18
     #~ 91.2917     23.4583   19
      #~ 91.375     22.7917   20

station_ids = [
 "01",
 "02",
 "03",
 "04",
 "05",
 "06",
 "07",
 "08",
 "09",
 "10",
 "11",
 "12",
 "13",
 "14",
 "15",
 "16",
 "17",
 "18",
 "19",
 "20"
]
station_latitudes  = [
     26.2083,
     26.0417,
     25.875,
     25.875,
     25.7917,
     25.7917,
     25.7083,
     25.125,
     24.9583,
     24.875,
     24.7083,
     24.625,
     24.4583,
     24.375,
     24.125,
     24.0417,
     24.0417,
     23.875,
     23.4583,
     22.7917
]
station_longitudes = [
     89.0417,
     89.7083,
     89.625,
     89.875,
     88.7083,
     89.4583,
     89.0417,
     89.7083,
     88.7917,
     92.5417,
     91.125,
     91.7083,
     88.2083,
     91.2083,
     89.625,
     89.0417,
     90.9583,
     91.2083,
     91.2917,
     91.375
]


# main output folder
main_output_folder = "/scratch-shared/edwin/data_for_tamim/daily_discharge/daily_txt/"

for i_rcp in range(0, len(rcp_codes)):
    
    rcp = rcp_codes[i_rcp]
    
    if rcp == "historical_baseline":
        gcm_small_names = ["watch"]
    else:
        rcp = "rcp" + rcp
    
    for i_gcm in range(0, len(gcm_small_names)):

        gcm_small_name = gcm_small_names[i_gcm]
        
        # output folder
        output_folder = main_output_folder + rcp + "/" + gcm_small_name + "/"
        os.system('rm -r ' + output_folder + "/*")
        try:
		    os.makedirs(output_folder)
        except:
	        pass
        os.chdir(output_folder)

        # netcdf file name
        # - example: "/scratch-shared/edwinhs/daily_discharge_aqueduct_flood_analyzer/m17/gfdl-esm2m/rcp8p5/discharge_dailyTot_output_1951-2099.nc4" 
        netcdf_input_file = main_input_folder + "/" + rcp + "/discharge_dailyTot*"
        
        # command line
        cmd = " "
        for i_station in range(0, len(station_ids)):
			
            station_id = station_ids[i_station]
            lat = station_latitudes[i_station]
            lon = station_latitudes[i_station]
            
            # cdo command
            #~ cdo outputtab,date,lon,lat,value -remapnn,lon=89.625_lat=25.0417 /scratch-shared/edwinhs/daily_discharge_aqueduct_flood_analyzer/m17/watch/historical_baseline/*annuaAvg*.nc > watch_BD_BRAHMAPUTRA_2651100_BAHADURABAD_table.txt
            cmd += " cdo outputtab,date,lon,lat,value -remapnn,lon=" + str(lon) + "_lat=" + str(lat) + " " + netcdf_input_file + " > " + rcp_code +"_" + gcm_small_name + "_" + station_id + "_table.txt & "

        cmd += " wait "
        print(cmd)
        os.system(cmd)

# Note that the total number of timesteps/days between 1951 and 2099 must be 54422. 
