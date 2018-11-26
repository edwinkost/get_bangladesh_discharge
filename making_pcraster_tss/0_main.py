#!/usr/bin/python
# -*- coding: utf-8 -*-

# EHS (24 September 2014): This is the main script for converting 
#                          a set of pcraster time series maps  
#                          into a single netcdf time series file. 
#
# EHS (27 November 2014): I use this script for converting EFAS-Meteo pcraster files to netcdf format

import os
import sys

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
netcdf_input_file = 

areaMapFileName,\
netcdf_input_clone_map_file, 
output_folder, \
unit_conversion_factor, \
modelTime, \
inputProjection, \
outputProjection, \
resample_method, \
tss_output_file):


# prepare the output folder
try:
    os.makedirs(output['folder'])
except:
    cmd = 
    os.system('rm -r ')

startDate     = "1990-01-01"
endDate       = ""

# projection/coordinate sy
inputEPSG  = "EPSG:3035" 
outputEPSG = "EPSG:4326"
resample_method = "near"

###########################################################################################################

def main():
    
    # prepare logger and its directory
    log_file_location = output['folder']+"/log/"
    try:
        os.makedirs(log_file_location)
    except:
        cmd = 'rm -r '+log_file_location+"/*"
        os.system(cmd)
        pass
    vos.initialize_logging(log_file_location)
    
    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate,endDate,nrOfTimeSteps)
    
    calculationModel = CalcFramework(cloneMapFileName,\
                                     pcraster_files, \
                                     modelTime, \
                                     output, inputEPSG, outputEPSG, resample_method)

    dynamic_framework = DynamicFramework(calculationModel,modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()

if __name__ == '__main__':
    sys.exit(main())
