

set -x

python merging_daily_discharge_watch.py  &

python merging_daily_discharge_gfdl-esm2m_rcp2p6.py &
python merging_daily_discharge_gfdl-esm2m_rcp4p5.py &
python merging_daily_discharge_gfdl-esm2m_rcp6p0.py &
python merging_daily_discharge_gfdl-esm2m_rcp8p5.py &

python merging_daily_discharge_hadgem2-es_rcp2p6.py &
python merging_daily_discharge_hadgem2-es_rcp4p5.py &
python merging_daily_discharge_hadgem2-es_rcp6p0.py &
python merging_daily_discharge_hadgem2-es_rcp8p5.py &

python merging_daily_discharge_ipsl-cm5a-lr_rcp2p6.py &
python merging_daily_discharge_ipsl-cm5a-lr_rcp4p5.py &
python merging_daily_discharge_ipsl-cm5a-lr_rcp6p0.py &
python merging_daily_discharge_ipsl-cm5a-lr_rcp8p5.py &

python merging_daily_discharge_miroc-esm-chem_rcp2p6.py &
python merging_daily_discharge_miroc-esm-chem_rcp4p5.py &
python merging_daily_discharge_miroc-esm-chem_rcp6p0.py &
python merging_daily_discharge_miroc-esm-chem_rcp8p5.py &

python merging_daily_discharge_noresm1-m_rcp2p6.py &
python merging_daily_discharge_noresm1-m_rcp4p5.py &
python merging_daily_discharge_noresm1-m_rcp6p0.py &
python merging_daily_discharge_noresm1-m_rcp8p5.py &

set +x

wait
