import os

import numpy as np

from datetime import datetime
from pyearth.toolbox.date.day_in_month import day_in_month
import pyearth.toolbox.date.julian as julian
from pyearth.toolbox.reader.text_reader_string import text_reader_string
cfs2cms = 0.028316847

#create the time series 
# URL for the water data service API
current_file_path = os.path.abspath(__file__)
print(current_file_path)
current_file_directory = os.path.dirname(current_file_path)
print(current_file_directory)

squaremile2squarekm = 2.58999
#define a leap year function

# USGS gage number for the stream of interest
aGage_num = ['BON', 'IHR']

aLon = []
aLat = []

#read the csv
sFilename = '/qfs/people/liao313/data/e3sm/columbia/mosart/BPA_NRNI_flow/NRNI_Flows_1929-2008_Corrected_04-2017.csv'

aData_all = text_reader_string(sFilename, cDelimiter_in = ',', iSkipline_in = 7)

aIndex = [24, 83]

aDate_raw = aData_all[:, 1]

nDate = len(aDate_raw)
aDate_obj = list()

for i in range(0, nDate):
    dummy = aDate_raw[i]
    dummy1 = dummy.split('-')
    
    iYear = int(dummy1[2])
    if iYear > 25:
        iYear = 1900 + iYear
    else:
        iYear = 2000 + iYear
    
    month_letter = dummy1[1] 
    iMonth = datetime.strptime(month_letter, '%b').month

    iDay = int(dummy1[0])
    dateobj = datetime(iYear,iMonth,iDay)
    aDate_obj.append(dateobj)

aDate_obj = np.array(aDate_obj)

iYear_start = 2000
iYear_end = 2019
aDate= list()

for iYear in range(iYear_start,iYear_end+1):
    for iMonth in range(1,13):
        #get day count in this month
        iDay_end = day_in_month(iYear, iMonth)
        for iDay in range(1,iDay_end+1):            
            aDate.append(datetime(iYear,iMonth,iDay))

aDate = np.array(aDate)

nDate = len(aDate)


for k in range(0, len(aGage_num)):
    gage_num = aGage_num[k]
    aData_out = np.full(nDate,  np.nan, dtype= float)
    for i in range(0, nDate):
        dateobj = aDate[i]
        lIndex = np.where(aDate_obj == dateobj)
        if len(lIndex[0]) == 0:
            pass
        else:           
            aData_out[i] = aData_all[lIndex, aIndex[k]]
        pass

    #save as text
    sFilename_out = '/qfs/people/liao313/data/e3sm/columbia/mosart/BPA_NRNI_flow/' +  gage_num + '.txt'
    np.savetxt(sFilename_out, aData_out * cfs2cms, fmt='%1.3f', delimiter=',')
   
    





