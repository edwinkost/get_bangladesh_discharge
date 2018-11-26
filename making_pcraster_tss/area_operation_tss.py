#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import time
import datetime

#~ from pcraster.framework import DynamicModel
from pcraster.framework import *

import pcraster as pcr
import numpy as np

import virtualOS as vos

import logging
logger = logging.getLogger(__name__)

class AreaOperationNetcdfToPCRasterTSS(DynamicModel):

    def __init__(self, netcdf_input_file, \
                       areaMapFileName,\
                       netcdf_input_clone_map_file, 
                       output_folder, \
                       unit_conversion_factor, \
                       modelTime, \
                       inputProjection, \
                       outputProjection, \
                       resample_method, \
                       tss_output_file_name):

        DynamicModel.__init__(self)
        
        # clone maps
        self.outputClone = areaMapFileName
        self.inputClone  = netcdf_input_clone_map_file
        
        # time variable/object
        self.modelTime = modelTime
        
        self.resample_method  = resample_method

        # output folder 
        self.output_folder = output_folder
        try:
            os.makedirs(self.output_folder)
        except:
            os.system('rm -r ' + self.output_folder +"/*")
        
        # prepare temporary directory
        self.tmpDir = self.output_folder + "/tmp/"
        try:
            os.makedirs(self.tmpDir)
        except:
            os.system('rm -r '+ tmpDir + "/*")
        
        # input and output projection/coordinate systems 
        self.inputProjection  =  inputProjection
        self.outputProjection = outputProjection
        
        # resample method

        # netcdf input file
        self.netcdf_input_file = netcdf_input_file

        # get the properties of 
        pcr.setclone(self.outputClone)
        self.cell_length  = pcr.clone().cellSize()
        self.x_min_output = pcr.clone().west()
        self.x_max_output = pcr.clone().west()  + pcraster.clone().nrCols() * pcr.clone().cellSize()
        self.y_min_output = pcr.clone().north() - pcraster.clone().nrRows() * pcr.clone().cellSize()
        self.y_max_output = pcr.clone().north()

        # pcraster area file
        self.area_class = pcr.readmap(areaMapFileName)
        # - landmask
        self.landmask = pcr.defined(self.area_class)
        self.landmask = pcr.ifthen(self.landmask, self.landmask)

        # object for daily tss reporting
        # - tss output file
        self.tss_daily_file = tss_output_file_name + "_daily"
        # - choose a point for each area as its representative
        self.point_area_class = pcr.ifthen(self.areaorder(pcr.scalar(self.area_class), self.area_class) == self.area_class, self.area_class)
        # - tss reporting object
        self.tss_reporting = TimeoutputTimeseries(self.tss_daily_file, self, self.area_class, noHeader = False)       

        # object for 10 day tss reporting
        # - tss output file
        self.tss_ten_day_file = tss_output_file_name + "_10days"
        # - tss reporting object
        self.tss_ten_day_reporting = TimeoutputTimeseries(self.tss_ten_day_file, self, self.area_class, noHeader = False)       


    def initial(self): 
        pass

    def dynamic(self):
        
        # re-calculate current model time using current pcraster timestep value
        self.modelTime.update(self.currentTimeStep())

        # read netcdf file
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
              '-s_srs ' + inputProjection  +" "+\
              '-t_srs ' + outputProjection +" "+\
              '-te ' + bound_box + " " +\
              '-tr ' + cell_size + " " +\
              '-r '+ self.resample_method + " " +\
              '-srcnodata -3.4028234663852886e+38 -dstnodata -3.4028234663852886e+38 '+\
              tmp_input_tif_file + " "+\
              tmp_reprj_tif_file
        print cmd ; os.system(cmd)
        # - convert it back to pcraster map
        tmp_reprj_map_file = self.tmpDir + "/" + "tmp_reprj_map.map"
        cmd = 'gdal_translate ' + tmp_reprj_tif_file + " " + tmp_reprj_map_file
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
        
        # save it to a daily tss file
        self.tss_reporting.sample(output_area_pcr)
        
        
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
             self.tss_ten_day_reporting(average_per_ten_days)
        
        # clean the temporary folder
        cmd = 'rm -r ' + self.tmpDir + "/*" 
        print cmd ; os.system(cmd)
