#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

# pcraster dynamic framework is used.
from pcraster.framework import DynamicFramework

# The calculation script (engine) is imported from the following module.
from area_operation_tss import AreaOperationNetcdfToPCRasterTSS

# time object
from currTimeStep import ModelTime

# utility module:
import virtualOS as vos

import logging
logger = logging.getLogger(__name__)


###########################################################################################################

# input is given in a netcdf file
netcdf_input_file = "/scratch-shared/edwinswt/from_edwin/data_for_tamim/forcing/netcdf/historical_baseline/watch/pr_watch_1958-2001.nc"
# - clone map for the netcdf input file 
netcdf_input_clone_map_file = "/home/edwinsut/github/edwinkost/get_bangladesh_discharge/making_pcraster_tss/files_from_tamim/bangladesh_clone_30min.map"

# start and end dates
startDate = "1958-01-01"
endDate   = "2001-12-31"
# - testing
startDate = "1990-01-01"
endDate   = "2001-12-31"


# unit conversion
unit_conversion_factor = 86.4 * 1000.0
unit_conversion_offset = 0.0            # for temperature (to Celcius), this will be -273.15
# - Note that there are three INPUT forcing variables: pr (precipitation, unit: kg.m-2.s-1), epot (reference potential evaporation, unit: m/day), and tas (surface air temperatue, unit: K)
# - Note that 1 kg.m-2.s-1 = 86.4 m.day-1, 
# - The OUTPUT units should be mm.day-1 for pr, degree Celcius for tas, and mm.day-1 for epot. 

# output folder
output_folder = "/scratch-shared/edwinsut/tss_forcing_for_tamin/test_final_for_demo/"

# tss output files (this will be relative to the output_folder)
tss_daily_output_file = "forcing_daily.tss"
tss_10day_output_file = "forcing_decad.tss"

# catchment/class pcraster map
# - the output clone will be based on this file
areaMapFileName = "/home/edwinsut/github/edwinkost/get_bangladesh_discharge/making_pcraster_tss/files_from_tamim/catchment_BD.map"
# - station/point map corresponding to areaMapFileName
areaPointMapFileName = "/home/edwinsut/github/edwinkost/get_bangladesh_discharge/making_pcraster_tss/files_from_tamim/catchment_BD_point.map"

# input and output projection system (GDAL/PRJ format)
inputProjection   = "EPSG:4326"
outputProjection  = "/home/edwinsut/github/edwinkost/get_bangladesh_discharge/making_pcraster_tss/files_from_tamim/catchment_BD_projection.prj"

# resampling method
resample_method = "near"



########################################################################################################################

def main():
    
    # - prepare the output folder
    if os.path.exists(output_folder): shutil.rmtree(output_folder)
    os.makedirs(output_folder)    

    # prepare logger and its directory
    log_file_location = output_folder + "/log/"
    os.makedirs(log_file_location)
    vos.initialize_logging(log_file_location)
    
    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate, endDate)
    
    #~ print modelTime.nrOfTimeSteps
    
    # calculation model/framework
    calculationModel = AreaOperationNetcdfToPCRasterTSS(netcdf_input_file = netcdf_input_file, \
                                                        areaMapFileName      = areaMapFileName, \
                                                        areaPointMapFileName = areaPointMapFileName, \
                                                        netcdf_input_clone_map_file = netcdf_input_clone_map_file, \
                                                        output_folder = output_folder, \
                                                        unit_conversion_factor = unit_conversion_factor, \
                                                        unit_conversion_offset = unit_conversion_offset, \
                                                        modelTime = modelTime, \
                                                        inputProjection  = inputProjection, \
                                                        outputProjection = outputProjection, \
                                                        resample_method  = resample_method, \
                                                        tss_daily_output_file = tss_daily_output_file, \
                                                        tss_10day_output_file = tss_10day_output_file, \
                                                        report_10day_pcr_files = True
                                                        )
    number_of_time_steps = modelTime.nrOfTimeSteps
    #~ number_of_time_steps = 100
    dynamic_framework = DynamicFramework(calculationModel, number_of_time_steps)
    dynamic_framework.setQuiet(True)
    # - start the calculation
    dynamic_framework.run()
    
    
    #~ # reformat 10 day tss file
    #~ # - change directory to the output folder so that the tss file will be stored there
    #~ os.chdir(self.output_folder)
    #~ # - open 10 day tss file
    #~ file_10day_tss = open(tss_10day_output_file, "r")
    #~ file_10day_tss_content = file_10day_tss.readlines()
    #~ # - get number of stations
    #~ number_of_stations = int(file_10day_tss_content[1].split("\n")[0])
    #~ # - save the header
    #~ header = file_10day_tss_content[0:number_of_stations + 2]
    #~ # - time series values
    #~ tss_complete = np.loadtxt(tss_10day_output_file, skiprows = number_of_stations + 2)
    #~ # - tss selected
    #~ first_column = tss_complete[:,1]
    #~ tss_filtered = tss_complete[np.where(first_column >= 0.0)[0], :] 
    #~ # - time series values in a formatted array
    #~ arr = np.ndarray(tss_filtered.shape, dtype = object)
    #~ arr[:,0] = range(1, tss_filtered.shape[0] + 1, 1)
    #~ arr[:,1:] = tss_filtered[:,1:]
    #~ # - write to a file
    #~ file_10day_tss_formatted = open(tss_10day_output_file + "_formatted.tss", "w")
    #~ for i in range(0, len(header)): file_10day_tss_formatted.write(header[i])
    #~ for i in range(0, len(arr[:,0])): file_10day_tss_formatted.write(arr[i,:])
    #~ file_10day_tss_formatted.close()
    
    
    

if __name__ == '__main__':
    sys.exit(main())

########################################################################################################################
