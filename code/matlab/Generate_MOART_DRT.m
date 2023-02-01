clear;close all;clc;

addpath('./Setup-E3SM-Mac/matlab-scripts-for-mosart');

basins = {'SUS','CRB','SAG'}; % SUS: Susquehanna river basin, 
                              % CRB: Columbia River Basin, 
                              % Sag: Sag river basin 
res    = {'8th','16th'};
debug  = 1;

for i = 1 %: length(res)
    if strcmp(res{i},'8th')
        dx = 1/8; dy = 1/8;
        fname = 'MOSART_global_8th_20180211c.nc';
        fdir  = '../../data/mosart/';
        ftemp = [fdir fname];
        url   = 'https://web.lcrc.anl.gov/public/e3sm/inputdata/rof/mosart/';
        cmd   = ['/usr/local/bin/wget -O ' ftemp ' ' url fname]; 
        if ~exist(ftemp,'file')
            [status,cmdout] = system(cmd,'-echo');
        end
        if exist(ftemp,'file')
            disp('Template MOSART input file downloads suscessfully!');
        else
            disp(['Cannot download ' fname ' from ' url]);
        end
    elseif strcmp(res{i},'16th')
    end
    for j = 1 %: length(basins)
        basin = basins{j};
        usrdat_name = [basin '_' res{i}]; % User defined name
        % Outlet coordinates
        if strcmp(basin,'SUS')
            xout   = -76.1741754;
            yout   = +39.6579133;
            Abasin = 27500*2.59e+6; %[m^2]
        elseif strcmp(basin,'CRB')
            
        elseif strcmp(basin,'SAG')
            
        end
        
        [iout, icon] = find_mosart_cell(ftemp,xout,yout,Abasin);
        in = [iout; icon];
        
        % Extract MOSART reginoal mesh from Global mesh
        if ~exist('inputdata','dir')
            mkdir('./inputdata');
        end
        fout1 = CreateMOSARTUgridInputForE3SM2(in, ftemp, './inputdata', usrdat_name);
        
        % Generate lnd domain file
        xc = ncread(fout1, 'longxy'); xv = zeros(4,length(xc));     
        yc = ncread(fout1, 'latixy'); yv = zeros(4,length(xc));
        xv(1,:) = xc - dx/2; xv(2,:) = xc + dx/2; 
        xv(3,:) = xc + dx/2; xv(4,:) = xc - dx/2; 
        yv(1,:) = yc - dx/2; yv(2,:) = yc - dx/2; 
        yv(3,:) = yc + dx/2; yv(4,:) = yc + dx/2; 
        frac = ncread(fout1, 'frac');
        mask = ones(length(frac),1);

        fout2 =  sprintf('%s/domain_lnd_%s_%s.nc','./inputdata',usrdat_name,datestr(now,'cyymmdd'));
        area  = generate_lnd_domain(xc,yc,xv,yv,frac,mask,[],fout2);

        if debug 
            longxy = ncread(fout1,'longxy');
            latixy = ncread(fout1,'latixy');
            figure;
            show_river_network(fout1,0);hold on;
            plot(longxy,latixy,'k.'); 
            title(basin,'FontSize',15,'FontWeight','bold');
        end
    end
end

