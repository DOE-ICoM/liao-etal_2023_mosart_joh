import numpy as np

def find_contributing_cells(aLongitude_in, aLatitude_in, aCellID, aCellID_downslope, area,  lon, lat, target_area):
    """
    Should the data in 2D? or MPAS based?
    """

    #find the cell what matches with drainage area?

    debug = 0
    iFlag_method = 2 # method 1: searching from each cell to see if it flows to the given outlet
    # method 2: searching from the outlet <- much quicker!


            
       
    aCellID_downslope=np.array(aCellID_downslope)
    nCell = aCellID_downslope.shape()
 

    aDistance = np.full(nCell, -9999, dtype=float)

    #calculate the distance betwen the cell with other cells

    for i in range(nCell):
        #this is a very simple function 
        dummy = np.power(aLongitude_in(i)- lon, 2) + np.power(aLatitude_in[i] - lat ,2)
        aDistance[i] = np.sqrt( dummy )
    
    aIndex_distance = np.argsort(aDistance)

    
    nSearch = 20
    

    for iSearch in range(nSearch):
        iIndex_dummy = aIndex_distance[iSearch]
        lCellID = aCellID[iIndex_dummy]

        aCell_contribution = list()

        if iFlag_method == 1:

            nTenth = np.ceil(0.1 * nCell)

            for i in range(nCell):

                if np.mod(i, nTenth) == 0:
                    dummy = '%0.3f'.format(i / nTenth * 10)
                    print(dummy)
                

                found = aCellID_downslope(i) == aCellID(outletg)
                j = i

                while (found) and (aCellID_downslope(j) != -9999):
                    j = np.where(aCellID == aCellID_downslope(j))
                    found = aCellID_downslope(j) == aCellID(outletg)
                

                if found:
                    icontributing.append( i)
        else:
            pass
            


        if target_area is not None:
            drainage_area = np.sum(   area[ioutlet, icontributing]  )
            #disp(drainage_area/2.59e+6);
            if (drainage_area / target_area > 0.5) and (drainage_area / target_area < 1.5):
                print('MOSART drainage area is ' + '%0.3f'.format(drainage_area / 1e6))
                print('GSIM drainage area is '+ '%0.3f'.format(target_area / 1e6))
         
     

    if target_area is not None:

        if drainage_area / target_area < 0.5 or drainage_area / target_area > 1.5:
            ioutlet = I(1)
            outletg = aCellID(ioutlet)
            icontributing = list()
            found = outletg

            while (found):
                found2 = list()

                for i in range(len(found)):
                    upstrm = np.where(aCellID_downslope == found(i))
                    found2.append( upstrm)
                

                icontributing = icontributing.append(found2)
                found = found2
      
    return ioutlet, icontributing


def get_geometry(xc, yc, aCellID, aCellID_downslope, area, aw, ad):
    """
    This is the function to retrive the river width, depth and 
    """
    #generate the mesh 
    nCell = len(xc)

    lon = np.arange(-179.75,179.75,0.5)
    lat = np.arange(-59.75,89.75, 0.5)
    lon, lat = np.meshgrid(lon, lat)


    lon = np.transpose(lon)
    lat = np.transpose(lat)

    aw = 7.2
    ad = 0.27
   
    runoff = np.full((len(xc), 31 * 365))
    discharge = np.full((len(xc), 31 * 365))
    AMF = np.full((len(xc), 31))
    k = 1
    print('Generating nearest neighbour mapping...')
    inear = np.full((len(xc), 1))
    onepercent = np.floor(len(xc) / 100);

    for i in range(len(xc)):

        if np.mod(i, onepercent) == 0:
            print(i / onepercent)
        else:
            if i == len(xc):
                print(' 100% \n')
        

        aDistance = np.sqrt(  np.power( lon - xc(i), 2) + np.power(lat - yc(i), 2) )
        
        ind = np.where(aDistance == np.min(aDistance))

        if len(ind)==0:
            print('Cannot find nearest neighbour!');
        else:
            if len(ind) > 1:
                print('grid cells are found!')
                print('*** Warning: This first one is used. ***')
                ind = ind(1)
        

        inear[i] = ind
    

    print('Reading daily runoff...\n')

    for i in range (1979,2009,1):

        if np.mod(i - 1979 + 1, 10) == 0:
            print('Year ' ,i)
        

        for j in range (1,365,1):
            #load(['/Users/xudo627/DATA/Runoff/runoff/RUNOFF05_' num2str(i) '_' num2str(j) '.mat']);
            #runoff[:, k] = ro05(inear)
            k = k + 1
        

    #index = cell(len(xc), 1)
    dummy = np.full( len(xc), -9999, dtype = 1 )
    print('Searching for contribuing area...\n')

    for i in range(0, nCell,1):

        if np.mod(i, onepercent) == 0:
            print(i / onepercent)
       

        [ioutlet, icontributing] = find_contributing_cells(xc, yc, aCellID, aCellID_downslope, area,  xc(i), yc(i))
        index[i] = [ioutlet; icontributing];
   

    print('Mapping runoff to discharge...\n');

    for i in range(1,len(xc),1):

       

        discharge[i, :] = np.sum(runoff(in[i], :) .* area(in[i]) ./ 1000 ./ (3 * 60 * 60), 1);


    for i in range (1,31,1):
        tmp = discharge[:, (i - 1) * 365 + 1:i * 365]
        AMF[:, i] = max(tmp, [], 2);
   

    flood_2yr = prctile(AMF, 50, 2);

    rwid = aw .* flood_2yr.^0.52
    rdep = ad .* flood_2yr.^0.31

    return rwid, rdep, flood_2yr