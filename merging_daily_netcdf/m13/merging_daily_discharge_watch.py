#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

clone_code = "M13"

folder_location = "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave/no_correction/non-natural/"

#~ edwinhs@fcn26.bullx:/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave/no_correction/non-natural$ ls -lah */M13/netcdf/discharge_dailyTot_output.nc 
#~ -r-xr-xr-x 1 edwinsut aqueduct 1.8G Nov 16  2016 begin_from_1958/M13/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 115M Nov 16  2016 begin_from_1958_only_test/M13/netcdf/discharge_dailyTot_output.nc - NOT USED
#~ -r-xr-xr-x 1 edwinsut aqueduct 909M Nov  1  2016 continue_from_1976/M13/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 1.7G Nov 16  2016 continue_from_1985/M13/netcdf/discharge_dailyTot_output.nc

# names of netcdf files that will be merged
netcdf_file_names = \
[
folder_location + "/begin_from_1958/"    + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
folder_location + "/continue_from_1976/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
folder_location + "/continue_from_1985/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
]

# time period for each netcdf file
start_years = ['1958', '1976', '1985']
end_years   = ['1975', '1984', '2001']

# output folder
output_folder = "/projects/0/dfguu2/scratch/edwin/daily_discharge_aqueduct_flood_analyzer/m13/watch/historical_baseline/"
# - make and go to the output folder
os.system('rm -r ' + output_folder + "/*")
try:
	os.makedirs(output_folder)
except:
	pass
os.chdir(output_folder)

# output netcdf file
output_netcdf_file = "discharge_dailyTot_output_" + start_years[0] + "-" + end_years[len(end_years)-1] + ".nc4"

# cdo command for merging
cmd = \
'cdo -L -f nc4 -z zip -mergetime ' +\
'-selyear,' + start_years[0] + "/" + end_years[0] + " " + netcdf_file_names[0] + " " +\
'-selyear,' + start_years[1] + "/" + end_years[1] + " " + netcdf_file_names[1] + " " +\
'-selyear,' + start_years[2] + "/" + end_years[2] + " " + netcdf_file_names[2] + " " +\
output_netcdf_file
print(cmd)
os.system(cmd)
