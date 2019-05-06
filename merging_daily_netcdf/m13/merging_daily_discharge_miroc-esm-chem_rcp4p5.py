#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

clone_code = "M13"

historical_folder_location = "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem/no_correction/non-natural/"

#~ edwinhs@fcn1.bullx:/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem/no_correction/non-natural$ ls -lah */M13/netcdf/discharge_dailyTot_output.nc 
#~ -r-xr-xr-x 1 edwinsut aqueduct 923M Nov 16  2016    begin_from_1951/M13/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 2.4G Nov 14  2016 continue_from_1960/M13/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 2.2G Nov 16  2016 continue_from_1984/M13/netcdf/discharge_dailyTot_output.nc

rcp_folder_location = "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem/no_correction/rcp4p5"

#~ edwinhs@fcn1.bullx:/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem/no_correction/rcp4p5$ ls -lah */M13/netcdf/discharge_dailyTot_output.nc 
#~ -r-xr-xr-x 1 edwinsut aqueduct 2.5G Nov  7  2016    begin_from_2006/M13/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct  99M Nov  8  2016 continue_from_2030/M13/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 295M Nov 16  2016 continue_from_2031/M13/netcdf/discharge_dailyTot_output.nc
#~ -r--r--r-- 1 edwinsut aqueduct 2.1G Dec 28  2016 continue_from_2033/M13/netcdf/discharge_dailyTot_output.nc
#~ -r--r--r-- 1 edwinsut aqueduct 3.1G Dec 29  2016 continue_from_2053/M13/netcdf/discharge_dailyTot_output.nc
#~ -r--r--r-- 1 edwinsut aqueduct 1.6G Dec 29  2016 continue_from_2084/M13/netcdf/discharge_dailyTot_output.nc

# names of netcdf files that will be merged
netcdf_file_names = \
[
historical_folder_location +    "/begin_from_1951/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
historical_folder_location + "/continue_from_1960/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
historical_folder_location + "/continue_from_1984/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        +    "/begin_from_2006/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/continue_from_2030/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/continue_from_2031/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/continue_from_2033/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/continue_from_2053/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/continue_from_2084/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
]

# time period for each netcdf file
start_years = [1951,\
               1960,\
               1984,\
               2006,\
               2030,\
               2031,\
               2033,\
               2053,\
               2084,\
               ]
end_years = []
for i in range(0, len(start_years)-1):
    end_years.append(start_years[i+1] - 1)
end_years.append(2099)

# output folder
output_folder = "/projects/0/dfguu2/scratch/edwin/daily_discharge_aqueduct_flood_analyzer/m13/miroc-esm-chem/rcp4p5/"
# - make and go to the output folder
#~ os.system('rm -r ' + output_folder + "/*")
try:
	os.makedirs(output_folder)
except:
	pass
os.chdir(output_folder)

# output netcdf file
output_netcdf_file = "discharge_dailyTot_output_" + str(start_years[0]) + "-" + str(end_years[len(end_years)-1]) + ".nc4"

# cdo command for merging
cmd = 'cdo -L -f nc4 -z zip -mergetime '
for i in range(0, len(start_years)):
	cmd = cmd + '-selyear,' + str(start_years[i]) + "/" + str(end_years[i]) + " " + netcdf_file_names[i] + " "
cmd = cmd + output_netcdf_file
print(cmd)
os.system(cmd)

# Note that the total number of timesteps/days between 1951 and 2099 must be 54422. 