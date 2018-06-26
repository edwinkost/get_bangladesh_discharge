
#~ cdo sellonlatbox,LON1,LON2,LAT1,LAT2 INAME ONAME

#~ to cut an area deﬁned by
#~ – LON1 and LON2 are the lower and upper longitude of your window
#~ – LAT1 and LAT2 the lower and upper latitiude of your window
#~ – INAME is your input ﬁlename
#~ – OUTPUT is your output ﬁlename

cdo sellonlatbox,87,95,20,28 /projects/0/dfguu/data/hydroworld/forcing/CMIP5/ISI-MIP-INPUT/GFDL-ESM2M/pr_bced_1960-1999_gfdl-esm2m_historical_1951-2005.nc bangladesh_pr_bced_1960-1999_gfdl-esm2m_historical_1951-2005.nc
