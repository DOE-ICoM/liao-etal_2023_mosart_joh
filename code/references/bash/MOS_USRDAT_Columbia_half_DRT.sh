#!/bin/sh

RES=MOS_USRDAT
COMPSET=RMOSGPCC
MACH=compy
COMPILER=intel
PROJECT=esmd

SRC_DIR=~/e3sm_test_snow
CASE_DIR=${SRC_DIR}/cime/scripts

cd ${SRC_DIR}/cime/scripts

GIT_HASH=`git log -n 1 --format=%h`
CASE_NAME=MOS_USRDAT_Columbia_half_DRT.`date "+%Y-%m-%d-%H%M%S"`

./create_newcase -case ${CASE_DIR}/${CASE_NAME} \
-res ${RES} -mach ${MACH} -compiler ${COMPILER} -compset ${COMPSET} --project ${PROJECT}


cd ${CASE_DIR}/${CASE_NAME}

./xmlchange -file env_run.xml -id DOUT_S             -val FALSE
./xmlchange -file env_run.xml -id INFO_DBUG          -val 2

./xmlchange CLM_USRDAT_NAME=test_r05_r05
./xmlchange LND_DOMAIN_FILE=domain_lnd_columbia_half_square_c201016.nc
./xmlchange ATM_DOMAIN_FILE=domain_lnd_columbia_half_square_c201016.nc
./xmlchange LND_DOMAIN_PATH=/qfs/people/xudo627/Columbia_Hexagon/inputdata
./xmlchange ATM_DOMAIN_PATH=/qfs/people/xudo627/Columbia_Hexagon/inputdata

./xmlchange DATM_CLMNCEP_YR_END=1979
./xmlchange DATM_CLMNCEP_YR_START=1979
./xmlchange DATM_CLMNCEP_YR_ALIGN=1979
./xmlchange DLND_CPLHIST_YR_START=1979
./xmlchange DLND_CPLHIST_YR_END=2008
./xmlchange DLND_CPLHIST_YR_ALIGN=1979
./xmlchange RUN_STARTDATE=1979-01-01

./xmlchange NTASKS=40
./xmlchange STOP_N=30,STOP_OPTION=nyears

./preview_namelists

cat >> user_nl_mosart << EOF
frivinp_rtm = '/qfs/people/xudo627/Columbia_Hexagon/inputdata/MOSART_columbia_half_square_c201016.nc'
EOF

cat >> user_nl_dlnd << EOF
dtlimit=2.0e0
EOF

./case.setup

files=""
for i in {1979..2007}
do
   files="${files}ming_daily_$i.nc\n"
done
files="${files}ming_daily_2008.nc"
echo "${files}"

cp ${CASE_DIR}/${CASE_NAME}/CaseDocs/dlnd.streams.txt.lnd.gpcc ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc
chmod +rw ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc
perl -w -i -p -e "s@/compyfs/inputdata/lnd/dlnd7/hcru_hcru@/compyfs/inputdata/lnd/dlnd7/mingpan@" ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc
perl -pi -e '$a=1 if(!$a && s/GPCC.daily.nc/ming_daily_1979.nc/);' {CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc
perl -w -i -p -e "s@GPCC.daily.nc@${files}@" ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc
sed -i '/ZBOT/d' ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc

#cp ${CASE_DIR}/${CASE_NAME}/CaseDocs/dlnd.streams.txt.lnd.gpcc ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc
#chmod +rw ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc
#perl -w -i -p -e "s@/compyfs/inputdata/lnd/dlnd7/hcru_hcru@/compyfs/inputdata/lnd/dlnd7/NLDAS@" ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc
#perl -w -i -p -e "s@GPCC.daily.nc@Livneh_NLDAS_1915_2011.nc@" ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc
#sed -i '/ZBOT/d' ${CASE_DIR}/${CASE_NAME}/user_dlnd.streams.txt.lnd.gpcc

./case.setup

./case.build

./case.submit