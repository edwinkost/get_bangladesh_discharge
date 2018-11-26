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

# unit conversion
unit_conversion_factor = 86.4 * 1000.0
unit_conversion_offset = 0.0
# - Note that there are three INPUT forcing variables: pr (precipitation, unit: kg.m-2.s-1), epot (potential evaporation, unit: m/day), and tas (surface air temperatue, unit: K)
# - Note that 1 kg.m-2.s-1 = 86.4 m.day-1, 
# - The OUTPUT units should be mm.day-1 for pr, degree Celcius for tas, and mm.day-1 for epot. 

# output folder
output_folder = "/scratch-shared/edwinsut/tss_forcing_for_tamin/test/"

# tss output files
tss_daily_output_file = output_folder + "/" + "forcing_daily.tss"
tss_10day_output_file = output_folder + "/" + "forcing_10day.tss"

# catchment/class pcraster map
# - the output clone will be based on this file
areaMapFileName = "/home/edwinsut/github/edwinkost/get_bangladesh_discharge/making_pcraster_tss/files_from_tamim/catchment_BD.map"

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
    
    print modelTime.nrOfTimeSteps
    
    # calculation model/framework
    calculationModel = AreaOperationNetcdfToPCRasterTSS(netcdf_input_file = netcdf_input_file, \
                                                        areaMapFileName   = areaMapFileName, \
                                                        netcdf_input_clone_map_file = netcdf_input_clone_map_file, \
                                                        output_folder = output_folder, \
                                                        unit_conversion_factor = unit_conversion_factor, \
                                                        unit_conversion_offset = unit_conversion_offset, \
                                                        modelTime = modelTime, \
                                                        inputProjection  = inputProjection, \
                                                        outputProjection = outputProjection, \
                                                        resample_method  = resample_method, \
                                                        tss_daily_output_file = tss_daily_output_file, \
                                                        tss_10day_output_file = tss_10day_output_file \
                                                        )
    dynamic_framework = DynamicFramework(calculationModel, modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    # - start the calculation
    dynamic_framework.run()
    
    # reformat 10 day tss file

if __name__ == '__main__':
    sys.exit(main())

########################################################################################################################
