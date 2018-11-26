#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

import time
import datetime

import numpy as np

import pcraster as pcr
from pcraster.framework import DynamicModel
from pcraster.framework import TimeoutputTimeseries

# time object
from currTimeStep import ModelTime

import virtualOS as vos

import logging
logger = logging.getLogger(__name__)

class AreaOperationNetcdfToPCRasterTSS(DynamicModel):

    def __init__(self, netcdf_input_file, \
                       areaMapFileName,\
                       netcdf_input_clone_map_file, \
                       output_folder, \
                       unit_conversion_factor, \
                       unit_conversion_offset, \
                       modelTime, \
                       inputProjection, \
                       outputProjection, \
                       resample_method, \
                       tss_daily_output_file, \
                       tss_10day_output_file, \
                       ):

        DynamicModel.__init__(self)
        
        # netcdf input file
        self.netcdf_input_file = netcdf_input_file

        # clone maps
        self.inputClone  = netcdf_input_clone_map_file
        self.outputClone = areaMapFileName
        
        # time variable/object
        self.modelTime = modelTime
        
        # output folder
        self.output_folder = output_folder
        
        # prepare temporary directory
        logger.info('Preparing tmp directory.')
        self.tmpDir = self.output_folder + "/tmp/"
        if os.path.exists(self.tmpDir): shutil.rmtree(self.tmpDir)
        os.makedirs(self.tmpDir)
        
        # input and output projection/coordinate systems 
        self.inputProjection  =  inputProjection
        self.outputProjection = outputProjection
        
        # resample method
        self.resample_method = resample_method
        
        # get the properties of output clone map (needed for resampling with gdalwarp)
        pcr.setclone(self.outputClone)
        self.cell_length  = pcr.clone().cellSize()
        self.x_min_output = pcr.clone().west()
        self.x_max_output = pcr.clone().west()  + pcr.clone().nrCols() * pcr.clone().cellSize()
        self.y_min_output = pcr.clone().north() - pcr.clone().nrRows() * pcr.clone().cellSize()
        self.y_max_output = pcr.clone().north()

        # pcraster area/class map
        self.area_class = pcr.readmap(areaMapFileName)
        # - landmask
        self.landmask = pcr.defined(self.area_class)
        self.landmask = pcr.ifthen(self.landmask, self.landmask)

        # objects for tss reporting
        # - choose a point for each area/class as its station representative
        self.point_area_class = pcr.nominal(pcr.ifthen(pcr.areaorder(pcr.scalar(self.area_class), self.area_class) == 1, self.area_class))
        pcr.aguila(self.point_area_class)
        raw_input("Press Enter to continue...")
        # - daily tss reporting object
        self.tss_daily_reporting = TimeoutputTimeseries("test", self, self.area_class, noHeader = False)       
        # - 10day tss reporting object
        self.tss_10day_reporting = TimeoutputTimeseries(tss_10day_output_file, self, self.area_class, noHeader = False)       


    def initial(self): 
        pass

    def dynamic(self):
        
        # re-calculate current model time using current pcraster timestep value
        self.modelTime.update(self.currentTimeStep())

        # read netcdf file
        logger.info("Reading netcdf file.")
        # - set the clone to the necdf file extent
        pcr.setclone(self.inputClone)
        # - read netcdf file
        input_pcr = vos.netcdf2PCRobjClone(ncFile = self.netcdf_input_file, \
                                           varName = "automatic", \
                                           dateInput = self.modelTime.fulldate, \
                                           useDoy = None, \
                                           cloneMapFileName  = self.inputClone, \
                                           LatitudeLongitude = True, \
                                           specificFillValue = None)
        
        # reprojection
        logger.info("Reprojection.")
        #
        # - save it to a pcraster file in the temporary folder
        tmp_input_pcr_file = self.tmpDir + "/" + "tmp_input_pcr.map"
        pcr.report(input_pcr, tmp_input_pcr_file)
        # - convert it to tif
        tmp_input_tif_file = self.tmpDir + "/" + "tmp_input_pcr.tif"
        cmd = 'gdal_translate ' + tmp_input_pcr_file + " " + tmp_input_tif_file
        print cmd ; os.system(cmd)
        # - re-projection to the outputProjection 
        tmp_reprj_tif_file = self.tmpDir + "/" + "tmp_reprj_tif.tif"
        bound_box = self.x_min_output + " " + self.y_min_output + " " + self.x_max_output + " " + self.y_max_output    
        cell_size = self.cell_length + " " + self.cell_length
        cmd = 'gdalwarp '+\
              '-s_srs ' + '"' + inputProjection  +'" '+\
              '-t_srs ' + '"' + outputProjection +'" '+\
              '-te ' + bound_box + " " +\
              '-tr ' + cell_size + " " +\
              '-r '+ self.resample_method + " " +\
              '-srcnodata -3.4028234663852886e+38 -dstnodata -3.4028234663852886e+38 '+\
              tmp_input_tif_file + " "+\
              tmp_reprj_tif_file
        print cmd ; os.system(cmd)
        # - convert it back to pcraster map
        tmp_reprj_map_file = self.tmpDir + "/" + "tmp_reprj_map.map"
        cmd = 'gdal_translate -of PCRaster' + tmp_reprj_tif_file + " " + tmp_reprj_map_file
        print cmd ; os.system(cmd)
        # - make sure that it has a valid mapattr
        cmd = 'mapattr -c ' + self.outputClone + " " + tmp_reprj_map_file
        print cmd ; os.system(cmd)
        
        
        # read the re-projected file
        # - set the clone to the output clone
        pcr.setclone(self.outputClone)
        output_pcr = pcr.readmap(tmp_reprj_map_file)
        # - unit conversion factor
        output_pcr = output_pcr * self.unit_conversion_factor
        pcr.aguila(output_pcr)
        raw_input("Press Enter to continue...")
        
        # perform area operation
        logger.info("Performing area operation.")
        output_area_pcr = pcr.areaaverage(output_pcr, self.area_class)
        pcr.aguila(output_pcr)
        raw_input("Press Enter to continue...")
        
        # save it to a daily tss file
        self.tss_daily_reporting.sample(output_area_pcr)
        
        # calculate 10 day average
        # - initiate/reset counter and accumulator
        if self.modelTime.day == 1 or self.modelTime.day == 11 or self.modelTime.day == 21:
            self.day_counter = 0.0
            self.cummulative_per_ten_days = pcr.scalar(0.0)
        # - accumulating
        self.day_counter = self.day_counter + 1
        self.cummulative_per_ten_days = self.cummulative_per_ten_days + output_area_pcr
        # - calculate 10 day average and reporting
        if self.modelTime.day == 10 or self.modelTime.day == 20 or self.modelTime.isLastDayOfMonth():
             logger.info('Saving 10 day average value.')
             average_per_ten_days = self.cummulative_per_ten_days / self.day_counter
             self.tss_10day_reporting(average_per_ten_days)
        
        # clean the temporary folder
        cmd = 'rm -r ' + self.tmpDir + "/*" 
        print cmd ; os.system(cmd)



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
