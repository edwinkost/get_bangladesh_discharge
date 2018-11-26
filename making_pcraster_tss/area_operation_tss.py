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
from pcraster.framework import TimeoutputTimeseries as TimeoutputTimeseries2

import virtualOS as vos

import logging
logger = logging.getLogger(__name__)

class AreaOperationNetcdfToPCRasterTSS(DynamicModel):

    def __init__(self, netcdf_input_file, \
                       areaMapFileName,\
                       areaPointMapFileName,\
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
        logger.debug('Preparing tmp directory.')
        self.tmpDir = self.output_folder + "/tmp/"
        if os.path.exists(self.tmpDir): shutil.rmtree(self.tmpDir)
        os.makedirs(self.tmpDir)
        
        # unit conversion variables
        self.unit_conversion_factor = unit_conversion_factor
        self.unit_conversion_offset = unit_conversion_offset
        
        # input and output projection/coordinate systems 
        self.inputProjection  =  inputProjection
        self.outputProjection = outputProjection
        
        # resample method
        self.resample_method = resample_method
        
        # get the properties of output clone map (in string, needed for resampling with gdalwarp command)
        pcr.setclone(self.outputClone)
        self.cell_length  = str(pcr.clone().cellSize()                                             )
        self.x_min_output = str(pcr.clone().west()                                                 )
        self.x_max_output = str(pcr.clone().west()  + pcr.clone().nrCols() * pcr.clone().cellSize())
        self.y_min_output = str(pcr.clone().north() - pcr.clone().nrRows() * pcr.clone().cellSize())
        self.y_max_output = str(pcr.clone().north()                                                )

        # pcraster area/class map
        self.area_class = pcr.readmap(areaMapFileName)
        # - landmask
        self.landmask = pcr.defined(self.area_class)
        self.landmask = pcr.ifthen(self.landmask, self.landmask)
        
        # - choose a point for each area/class as its station representative (needed for tss reporting)
        if areaPointMapFileName == None:
            logger.info("Get stations/representatives for all classes")
            self.point_area_class = pcr.nominal(pcr.ifthen(pcr.areaorder(pcr.scalar(self.area_class), self.area_class) == 1, self.area_class))
            #~ pcr.aguila(self.point_area_class)
            #~ raw_input("Press Enter to continue...")
        else:
            self.point_area_class = pcr.readmap(areaPointMapFileName)
            self.point_area_class = pcr.ifthen(self.landmask, self.point_area_class)    
        
        # output tss file
        self.tss_daily_output_file = tss_daily_output_file
        self.tss_10day_output_file = tss_10day_output_file


    def initial(self): 

        # objects for tss reporting
        logger.debug("Preparing tss files.")
        # - daily tss reporting object
        self.tss_daily_reporting = TimeoutputTimeseries(self.tss_daily_output_file, self, self.area_class, noHeader = False)       
        # - 10day tss reporting object
        self.tss_10day_reporting = TimeoutputTimeseries2(self.tss_10day_output_file, self, self.area_class, noHeader = False)       

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
        logger.debug(cmd); os.system(cmd)
        # - re-projection to the outputProjection 
        tmp_reprj_tif_file = self.tmpDir + "/" + "tmp_reprj_tif.tif"
        bound_box = self.x_min_output + " " + self.y_min_output + " " + self.x_max_output + " " + self.y_max_output    
        cell_size = self.cell_length + " " + self.cell_length
        cmd = 'gdalwarp '+\
              '-s_srs ' + '"' + self.inputProjection  +'" '+\
              '-t_srs ' + '"' + self.outputProjection +'" '+\
              '-te ' + bound_box + " " +\
              '-tr ' + cell_size + " " +\
              '-r '+ self.resample_method + " " +\
              '-srcnodata -3.4028234663852886e+38 -dstnodata -3.4028234663852886e+38 '+\
              tmp_input_tif_file + " "+\
              tmp_reprj_tif_file
        logger.debug(cmd); os.system(cmd)
        # - convert it back to pcraster map
        tmp_reprj_map_file = self.tmpDir + "/" + "tmp_reprj_map.map"
        cmd = 'gdal_translate -of PCRaster ' + tmp_reprj_tif_file + " " + tmp_reprj_map_file
        logger.debug(cmd); os.system(cmd)
        # - make sure that it has a valid mapattr
        cmd = 'mapattr -c ' + self.outputClone + " " + tmp_reprj_map_file
        logger.debug(cmd); os.system(cmd)
        
        
        # read the re-projected file
        logger.info("Read the re-projected file, including unit conversion/correction.")
        # - set the clone to the output clone
        pcr.setclone(self.outputClone)
        output_pcr = pcr.readmap(tmp_reprj_map_file)
        # - unit conversion
        output_pcr = output_pcr * self.unit_conversion_factor + self.unit_conversion_offset
        #~ pcr.aguila(output_pcr)
        #~ raw_input("Press Enter to continue...")
        
        
        # perform area operation
        logger.info("Performing area operation.")
        output_area_pcr = pcr.areaaverage(output_pcr, self.area_class)
        #~ pcr.aguila(output_area_pcr)
        #~ raw_input("Press Enter to continue...")
        
        # save it to a daily tss file
        logger.info("Saving daily value to a tss file.")
        self.tss_daily_reporting.sample(output_area_pcr)
        
        # calculate 10 day average
        # - initiate/reset counter and accumulator
        if self.modelTime.day == 1 or self.modelTime.day == 11 or self.modelTime.day == 21:
            self.day_counter = 0.0
            self.cummulative_per_ten_days = pcr.scalar(0.0)
            self.average_per_ten_days = pcr.scalar(0.0)
        # - accumulating
        self.day_counter = self.day_counter + 1.0
        self.cummulative_per_ten_days = self.cummulative_per_ten_days + output_area_pcr
        # - calculate 10 day average and reporting
        if self.modelTime.day == 10 or self.modelTime.day == 20 or self.modelTime.isLastDayOfMonth():
             logger.info('Saving 10 day average value to a tss file.')
             average_per_ten_days = self.cummulative_per_ten_days / self.day_counter
        else:
             average_per_ten_days = pcr.scalar(-9999.0)
        self.tss_10day_reporting(average_per_ten_days)
        
        # clean the temporary folder
        cmd = 'rm -r ' + self.tmpDir + "/*" 
        print cmd ; os.system(cmd)

