cd /scratch-shared/edwin/data_for_tamim/forcing/netcdf/historical_baseline/watch/

cdo -L -f nc4 -z zip -sellonlatbox,87,95,20,28 /projects/0/dfguu/data/hydroworld/forcing/WATCH/pr_total_gpcc_watch_1958-2001.nc4 pr_watch_1958-2001.nc
cdo -L -f nc4 -z zip -sellonlatbox,87,95,20,28 /projects/0/dfguu/data/hydroworld/forcing/WATCH/epot_watch_1958_2001.nc epot_watch_1958-2001.nc
cdo -L -f nc4 -z zip -sellonlatbox,87,95,20,28 /projects/0/dfguu/data/hydroworld/forcing/WATCH/tas_watch_1958-2001.nc4 tas_watch_1958-2001.nc
