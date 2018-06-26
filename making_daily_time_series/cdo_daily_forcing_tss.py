#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

main_input_folder = "/scratch-shared/edwin/data_for_tamim/forcing/netcdf/"

rcp_codes = ["2p6", "4p5", "6p0", "8p5", "historical_baseline"]
#~ rcp_codes = ["2p6"]

#~ gcm_names       = ["GFDL-ESM2M", "HadGEM2-ES", "IPSL-CM5A-LR", "MIROC-ESM-CHEM", "NorESM1-M"]
#~ gcm_names       = ["GFDL-ESM2M"]
gcm_small_names    = ["gfdl-esm2m", "hadgem2-es", "ipsl-cm5a-lr", "miroc-esm-chem", "noresm1-m"]
#~ gcm_small_names = ["gfdl-esm2m"]

variable_names  = ["epot", "pr", "tas"]

# station ids and coordinates (forcing)
       #~ 88.25       26.75    1
       #~ 88.75       26.75    2
       #~ 88.25       26.25    3
       #~ 88.75       26.25    4
       #~ 89.25       26.25    5
       #~ 89.75       26.25    6
       #~ 88.25       25.75    7
       #~ 88.75       25.75    8
       #~ 89.25       25.75    9
       #~ 89.75       25.75   10
       #~ 88.25       25.25   11
       #~ 88.75       25.25   12
       #~ 89.25       25.25   13
       #~ 89.75       25.25   14
       #~ 90.25       25.25   15
       #~ 90.75       25.25   16
       #~ 91.25       25.25   17
       #~ 91.75       25.25   18
       #~ 92.25       25.25   19
       #~ 92.75       25.25   20
       #~ 88.25       24.75   21
       #~ 88.75       24.75   22
       #~ 89.25       24.75   23
       #~ 89.75       24.75   24
       #~ 90.25       24.75   25
       #~ 90.75       24.75   26
       #~ 91.25       24.75   27
       #~ 91.75       24.75   28
       #~ 92.25       24.75   29
       #~ 92.75       24.75   30
       #~ 88.25       24.25   31
       #~ 88.75       24.25   32
       #~ 89.25       24.25   33
       #~ 89.75       24.25   34
       #~ 90.25       24.25   35
       #~ 90.75       24.25   36
       #~ 91.25       24.25   37
       #~ 91.75       24.25   38
       #~ 92.25       24.25   39
       #~ 92.75       24.25   40
       #~ 88.75       23.75   41
       #~ 89.25       23.75   42
       #~ 89.75       23.75   43
       #~ 90.25       23.75   44
       #~ 90.75       23.75   45
       #~ 91.25       23.75   46
       #~ 91.75       23.75   47
       #~ 92.25       23.75   48
       #~ 92.75       23.75   49
       #~ 88.75       23.25   50
       #~ 89.25       23.25   51
       #~ 89.75       23.25   52
       #~ 90.25       23.25   53
       #~ 90.75       23.25   54
       #~ 91.25       23.25   55
       #~ 91.75       23.25   56
       #~ 92.25       23.25   57
       #~ 92.75       23.25   58
       #~ 88.75       22.75   59
       #~ 89.25       22.75   60
       #~ 89.75       22.75   61
       #~ 90.25       22.75   62
       #~ 90.75       22.75   63
       #~ 91.25       22.75   64
       #~ 91.75       22.75   65
       #~ 92.25       22.75   66
       #~ 92.75       22.75   67
       #~ 88.75       22.25   68
       #~ 89.25       22.25   69
       #~ 89.75       22.25   70
       #~ 90.25       22.25   71
       #~ 90.75       22.25   72
       #~ 91.25       22.25   73
       #~ 91.75       22.25   74
       #~ 92.25       22.25   75
       #~ 92.75       22.25   76
       #~ 88.75       21.75   77
       #~ 89.25       21.75   78
       #~ 89.75       21.75   79
       #~ 90.25       21.75   80
       #~ 90.75       21.75   81
       #~ 91.25       21.75   82
       #~ 91.75       21.75   83
       #~ 92.25       21.75   84
       #~ 92.75       21.75   85
       #~ 91.75       21.25   86
       #~ 92.25       21.25   87
       #~ 92.75       21.25   88
       #~ 92.25       20.75   89

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
 "20",
 "21",
 "22",
 "23",
 "24",
 "25",
 "26",
 "27",
 "28",
 "29",
 "30",
 "31",
 "32",
 "33",
 "34",
 "35",
 "36",
 "37",
 "38",
 "39",
 "40",
 "41",
 "42",
 "43",
 "44",
 "45",
 "46",
 "47",
 "48",
 "49",
 "50",
 "51",
 "52",
 "53",
 "54",
 "55",
 "56",
 "57",
 "58",
 "59",
 "60",
 "61",
 "62",
 "63",
 "64",
 "65",
 "66",
 "67",
 "68",
 "69",
 "70",
 "71",
 "72",
 "73",
 "74",
 "75",
 "76",
 "77",
 "78",
 "79",
 "80",
 "81",
 "82",
 "83",
 "84",
 "85",
 "86",
 "87",
 "88",
 "89" 
]
station_latitudes  = [
 26.75,
 26.75,
 26.25,
 26.25,
 26.25,
 26.25,
 25.75,
 25.75,
 25.75,
 25.75,
 25.25,
 25.25,
 25.25,
 25.25,
 25.25,
 25.25,
 25.25,
 25.25,
 25.25,
 25.25,
 24.75,
 24.75,
 24.75,
 24.75,
 24.75,
 24.75,
 24.75,
 24.75,
 24.75,
 24.75,
 24.25,
 24.25,
 24.25,
 24.25,
 24.25,
 24.25,
 24.25,
 24.25,
 24.25,
 24.25,
 23.75,
 23.75,
 23.75,
 23.75,
 23.75,
 23.75,
 23.75,
 23.75,
 23.75,
 23.25,
 23.25,
 23.25,
 23.25,
 23.25,
 23.25,
 23.25,
 23.25,
 23.25,
 22.75,
 22.75,
 22.75,
 22.75,
 22.75,
 22.75,
 22.75,
 22.75,
 22.75,
 22.25,
 22.25,
 22.25,
 22.25,
 22.25,
 22.25,
 22.25,
 22.25,
 22.25,
 21.75,
 21.75,
 21.75,
 21.75,
 21.75,
 21.75,
 21.75,
 21.75,
 21.75,
 21.25,
 21.25,
 21.25,
 20.75
]
station_longitudes = [
 88.25,
 88.75,
 88.25,
 88.75,
 89.25,
 89.75,
 88.25,
 88.75,
 89.25,
 89.75,
 88.25,
 88.75,
 89.25,
 89.75,
 90.25,
 90.75,
 91.25,
 91.75,
 92.25,
 92.75,
 88.25,
 88.75,
 89.25,
 89.75,
 90.25,
 90.75,
 91.25,
 91.75,
 92.25,
 92.75,
 88.25,
 88.75,
 89.25,
 89.75,
 90.25,
 90.75,
 91.25,
 91.75,
 92.25,
 92.75,
 88.75,
 89.25,
 89.75,
 90.25,
 90.75,
 91.25,
 91.75,
 92.25,
 92.75,
 88.75,
 89.25,
 89.75,
 90.25,
 90.75,
 91.25,
 91.75,
 92.25,
 92.75,
 88.75,
 89.25,
 89.75,
 90.25,
 90.75,
 91.25,
 91.75,
 92.25,
 92.75,
 88.75,
 89.25,
 89.75,
 90.25,
 90.75,
 91.25,
 91.75,
 92.25,
 92.75,
 88.75,
 89.25,
 89.75,
 90.25,
 90.75,
 91.25,
 91.75,
 92.25,
 92.75,
 91.75,
 92.25,
 92.75,
 92.25
]


# main output folder
main_output_folder = "/scratch-shared/edwin/data_for_tamim/forcing/daily_txt/"

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

        for i_station in range(0, len(station_ids)):
			
            station_id = station_ids[i_station]
            lat =  station_latitudes[i_station]
            lon = station_longitudes[i_station]
            
            # command line
            cmd = " "
            for variable in variable_names:

                # netcdf file name
                # - example: "/scratch-shared/edwinhs/daily_discharge_aqueduct_flood_analyzer/m17/gfdl-esm2m/rcp8p5/discharge_dailyTot_output_1951-2099.nc4" 
                netcdf_input_file = main_input_folder + "/" + gcm_small_name + "/" + rcp + "/" + variable + "*"

                # cdo command
                #~ cdo outputtab,date,lon,lat,value -remapnn,lon=89.625_lat=25.0417 /scratch-shared/edwinhs/daily_discharge_aqueduct_flood_analyzer/m17/watch/historical_baseline/*annuaAvg*.nc > watch_BD_BRAHMAPUTRA_2651100_BAHADURABAD_table.txt
                cmd += " cdo outputtab,date,lon,lat,value -remapnn,lon=" + str(lon) + "_lat=" + str(lat) + " " + netcdf_input_file + " > " + rcp +"_" + gcm_small_name + "_" + station_id + "_table.txt & "

        cmd += " wait "
        print(cmd)
        os.system(cmd)

# Note that the total number of timesteps/days between 1951 and 2099 must be 54422. 
