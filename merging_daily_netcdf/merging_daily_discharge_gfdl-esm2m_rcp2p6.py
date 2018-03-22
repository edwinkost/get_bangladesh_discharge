#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

clone_code = "M17"

historical_folder_location = "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/non-natural/"

#~ edwinhs@fcn26.bullx:/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/non-natural$ ls -lah */M17/netcdf/discharge_dailyTot_output.nc 
#~ -r-xr-xr-x 1 edwinsut aqueduct 700M Nov 16  2016 begin_from_1951/M17/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 3.0G Nov 14  2016 continue_from_1958/M17/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 219M Nov 16  2016 continue_from_1988/M17/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 1.6G Nov 16  2016 continue_from_1990/M17/netcdf/discharge_dailyTot_output.nc

rcp_folder_location = "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_may_jun_rcp2p6/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/rcp2p6/"

#~ edwinhs@fcn26.bullx:/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_may_jun_rcp2p6/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/rcp2p6$ ls -lah */M17/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 496M Oct 24 21:25 begin_from_2006/M17/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 695M Oct 24 21:40 continue_from_2011/M17/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 3.1G Oct 24 22:08 continue_from_2017/M17/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 3.1G Oct 24 23:10 continue_from_2048/M17/netcdf/discharge_dailyTot_output.nc
#~ -r-xr-xr-x 1 edwinsut aqueduct 2.1G Oct 25 00:05 continue_from_2079/M17/netcdf/discharge_dailyTot_output.nc

# names of netcdf files that will be merged
netcdf_file_names = \
[
historical_folder_location + "/begin_from_1951/"    + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
historical_folder_location + "/continue_from_1958/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
historical_folder_location + "/continue_from_1988/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
historical_folder_location + "/continue_from_1990/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/begin_from_2006/"    + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/continue_from_2011/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/continue_from_2017/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/continue_from_2048/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
rcp_folder_location        + "/continue_from_2079/" + clone_code + "/netcdf/discharge_dailyTot_output.nc", \
]

# time period for each netcdf file
start_years = ['1951', '1958', '1988', '1990', '2006', '2011', '2017', '2048', '2079']
end_years   = ['1957', '1987', '1989', '2005', '2010', '2016', '2047', '2078', '2099']

# output folder
output_folder = "/scratch-shared/edwinhs/daily_discharge_aqueduct_flood_analyzer/m17/gfdl-esm2m/rcp2p6/"
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
