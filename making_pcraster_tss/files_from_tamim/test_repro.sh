gdalwarp -s_srs "EPSG:4326" -t_srs catchment_BD_projection.prj -te 298299 277148 779298 947148 -tr 1000 1000 test.tif test_reprj.tif

