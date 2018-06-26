#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

main_input_folder = "/projects/0/dfguu/data/hydroworld/forcing/CMIP5/ISI-MIP-INPUT"

rcp_codes = ["2p6", "4p5", "6p0", "8p5"]
#~ rcp_codes = ["2p6"]

gcm_names       = ["GFDL-ESM2M", "HadGEM2-ES", "IPSL-CM5A-LR", "MIROC-ESM-CHEM", "NorESM1-M"]
gcm_small_names = ["gfdl-esm2m", "hadgem2-es", "ipsl-cm5a-lr", "miroc-esm-chem", "noresm1-m"]
#~ gcm_names       = ["GFDL-ESM2M"]
#~ gcm_small_names = ["gfdl-esm2m"]

variable_names  = ["epot", "pr", "tas"]

# coordinates (used in cdo sellonlatbox,LON1,LON2,LAT1,LAT2 INAME ONAME)
sellonlatbox_coordinates = "87,95,20,28"

# main output folder
main_output_folder = "/scratch-shared/edwin/forcing/netcdf/"


for rcp in rcp_codes:

    for i_gcm in range(0, len(gcm_names)):
        gcm_name = gcm_names[i_gcm]
        gcm_small_name = gcm_small_names[i_gcm]

        # output folder
        output_folder = "/scratch-shared/edwin/forcing/netcdf/" + rcp + "/" + gcm_small_name + "/"
        os.system('rm -r ' + output_folder + "/*")
        try:
		    os.makedirs(output_folder)
        except:
	        pass
        os.chdir(output_folder)

        for variable in variable_names:
			
            # historical file name, example: NorESM1-M/pr_bced_1960-1999_noresm1-m_historical_1951-2005.nc
            historical_file = main_input_folder + "/" + gcm_name + "/" + variable + "_bced_1960*_" + gcm_small_name + "_*1951*.nc"
            
            # rcp file name, example:       GFDL-ESM2M/epot_bced_1960_1999_gfdl-esm2m_6p0_2006-2099.nc
            rcp_file = main_input_folder + "/" + gcm_name + "/" + variable + "_bced_1960*_" + gcm_small_name + "_" + rcp + "_2006*.nc"
            
            # output file name
            output_file = output_folder + "/" + variable + "_bced_1960-1999_" + gcm_small_name + "_" + "rcp" + rcp + "_1951-2099.nc"
            
            # cdo command for sellonlatbox
            # - example: cdo -L -f nc4 -z zip -mergetime -sellonlatbox,87,95,20,28 /projects/0/dfguu/data/hydroworld/forcing/CMIP5/ISI-MIP-INPUT/GFDL-ESM2M/tas_bced_1960-1999_gfdl-esm2m_historical_1951-2005.nc -sellonlatbox,87,95,20,28 /projects/0/dfguu/data/hydroworld/forcing/CMIP5/ISI-MIP-INPUT/GFDL-ESM2M/tas_bced_1960-1999_gfdl-esm2m_2p6_2006-2099.nc /scratch-shared/edwin/forcing/netcdf/2p6/gfdl-esm2m//tas_bced_1960-1999_gfdl-esm2m_2p6_1951-2099.nc
            # 
            cmd  = ' cdo -L -f nc4 -z zip -mergetime ' 
            cmd += '-sellonlatbox,' + sellonlatbox_coordinates + ' ' + historical_file + ' '
            cmd += '-sellonlatbox,' + sellonlatbox_coordinates + ' ' + rcp_file + ' '
            cmd += output_file
            print(cmd)
            os.system(cmd)

# Note that the total number of timesteps/days between 1951 and 2099 must be 54422. 
