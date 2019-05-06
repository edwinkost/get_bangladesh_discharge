#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# main output folder
main_output_folder = "/projects/0/dfguu2/scratch/edwin/daily_discharge_aqueduct_flood_analyzer/m13/txt/version_20190506/"

# main input folder
main_input_folder = "/projects/0/dfguu2/scratch/edwin/daily_discharge_aqueduct_flood_analyzer/m13/netcdf/"

rcp_codes = ["2p6", "4p5", "6p0", "8p5", "historical_baseline"]
#~ rcp_codes = ["2p6"]

#~ gcm_names       = ["GFDL-ESM2M", "HadGEM2-ES", "IPSL-CM5A-LR", "MIROC-ESM-CHEM", "NorESM1-M"]
#~ gcm_names       = ["GFDL-ESM2M"]
gcm_small_names    = ["gfdl-esm2m", "hadgem2-es", "ipsl-cm5a-lr", "miroc-esm-chem", "noresm1-m"]
#~ gcm_small_names = ["gfdl-esm2m"]


station_ids = [
 "01"
]
station_latitudes  = [
     12.4592
]
station_longitudes = [
    106.032
]

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
        netcdf_input_file = main_input_folder + "/" + gcm_small_name + "/" + rcp + "/discharge_dailyTot*"
        
        # command line
        cmd = " "
        for i_station in range(0, len(station_ids)):
			
            station_id = station_ids[i_station]
            lat =  station_latitudes[i_station]
            lon = station_longitudes[i_station]
            
            # cdo command
            #~ cdo outputtab,date,lon,lat,value -remapnn,lon=89.625_lat=25.0417 /scratch-shared/edwinhs/daily_discharge_aqueduct_flood_analyzer/m17/watch/historical_baseline/*annuaAvg*.nc > watch_BD_BRAHMAPUTRA_2651100_BAHADURABAD_table.txt
            cmd += " cdo outputtab,date,lon,lat,value -remapnn,lon=" + str(lon) + "_lat=" + str(lat) + " " + netcdf_input_file + " > " + rcp +"_" + gcm_small_name + "_" + station_id + "_table.txt & "

        cmd += " wait "
        print(cmd)
        os.system(cmd)

# Note that the total number of timesteps/days between 1951 and 2099 must be 54422. 
