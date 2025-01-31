clear;close all;clc;

addpath('/Users/xudo627/donghui/mylib/m/');
addpath('./Setup-E3SM-Mac/matlab-scripts-for-mosart');
addpath('./Setup-E3SM-Mac/matlab-scripts-to-process-inputs');

basins = {'SUS','CRB','SAG','AMZ'}; % SUS: Susquehanna river basin, 
                                    % CRB: Columbia River Basin, 
                                    % Sag: Sag river basin 
                                    % Amz: Amazon river basin
res    = {'half','8th','16th'};
debug  = 1;
wg     = '/usr/local/bin/wget';

for i = 2 %: length(res)
    if strcmp(res{i},'half')
        dx = 1/2; dy = 1/2;
        [ftemp, ftemp2] = download_temp(res{i},wg);
    elseif strcmp(res{i},'8th')
        dx = 1/8; dy = 1/8;
        ftemp = download_temp(res{i},wg);
    elseif strcmp(res{i},'16th')
        ftemp = download_temp('8th',wg);
        [fdir,flen,facc] = download_DRT(wg);
        [fd, X, Y] = ascread(fdir,[]);
        [fl, ~, ~] = ascread(flen,[]);
        [fa, ~, ~] = ascread(facc,[]);
        fd = flipud(fd);
        fl = flipud(fl);
        fa = flipud(fa);
        X    = flipud(X);
        Y    = flipud(Y);
    end
    for j = 4 %: length(basins)
        basin = basins{j};
        usrdat_name = [basin '_' res{i}]; % User defined name
        % Outlet coordinates
        if strcmp(basin,'SUS')
            xout   = -76.1741754;
            yout   = +39.6579133;
            Abasin = 27500*2.59e+6; %[m^2]
        elseif strcmp(basin,'CRB')
            xout   = -123.46834;
            yout   = +46.261050;
            Abasin = 257916*2.59e+6; %[m^2]
        elseif strcmp(basin,'SAG')
%             xout   = -148.19383;
%             yout   = +70.340000;
            xout =  -148.1875;
            yout = 70.1875;
            Abasin = 14900*1e+6; %[m^2]
        elseif strcmp(basin,'AMZ')
            xout   = -51.1250;
            yout   = -0.6875;
            Abasin = 6000000*1e6;
        end
        
        % Extract MOSART reginoal mesh from Global mesh
        if ~exist('inputdata','dir')
            mkdir('./inputdata');
        end
        
        if strcmp(res{i},'16th')
            [m, n] = size(fd);
            ID = 1 : length(fd(:));
            ID = reshape(ID',[m,n]);
            dnID = ones(m,n) .* -9999;
            
            for ii = 1 : m
                disp([num2str(ii) '/' num2str(m)]);
                for jj = 1 : n
                    if fd(ii,jj) == 1
                        dnID(ii,jj) = ID(ii,jj+1);
                    elseif fd(ii,jj) == 2
                        dnID(ii,jj) = ID(ii+1,jj+1);
                    elseif fd(ii,jj) == 4
                        dnID(ii,jj) = ID(ii+1,jj);
                    elseif fd(ii,jj) == 8
                        dnID(ii,jj) = ID(ii+1,jj-1);
                    elseif fd(ii,jj) == 16
                        dnID(ii,jj) = ID(ii,jj-1);
                    elseif fd(ii,jj) == 32
                        dnID(ii,jj) = ID(ii-1,jj-1);
                    elseif fd(ii,jj) == 64
                        dnID(ii,jj) = ID(ii-1,jj);
                    elseif fd(ii,jj) == 128
                        dnID(ii,jj) = ID(ii-1,jj+1);
                    end
                end
            end
            if strcmp(basin,'AMZ') && exist('drt_AMZ.mat','file')
                load('drt_AMZ.mat');
            else
                drt = struct([]);
                drt(1).dnID   = dnID;
                drt(1).ID     = ID;
                drt(1).longxy = X;
                drt(1).latixy = Y;
                [xv,yv,area] = xc2xv(X,Y,1/16,1/16,1);
                drt(1).area = area;
                [ioutlet, icontributing] = find_mosart_cell(drt,xout,yout,Abasin);
                
            
                idx = [ioutlet;icontributing];
                ID_region = 1 : length(idx);
                ID_region = ID_region';
                dnID_temp = dnID(idx);
                ID_temp   = ID(idx);
                dnID_region = NaN(length(dnID_temp),1);
                for ii = 1 : length(dnID_temp)
                    if dnID_temp(ii) == -9999
                        dnID_region(ii) = -9999;
                    else
                        ind = find(ID_temp == dnID_temp(ii));
                        if isempty(ind)
                            dnID_region(ii) = -9999;
                        else
                            dnID_region(ii) = ID_region(ind);
                        end
                    end
                end
                
                [xv,yv,area] = xc2xv(X(idx),Y(idx),1/16,1/16,1);
                
                clear drt;
                drt = struct([]);
                drt(1).longxy = X(idx);
                drt(1).latixy = Y(idx);
                drt(1).xv     = xv;
                drt(1).yv     = yv;
                drt(1).area   = area;
                drt(1).ID     = ID_region;
                drt(1).dnID   = dnID_region;
                drt(1).facc   = fa(idx);
                drt(1).flen   = fl(idx);
                drt(1).geometry_file = ['./Channel_geometry_DRT_' usrdat_name '.mat'];
                if strcmp(basin,'AMZ')
                    save('drt_AMZ.mat','drt')
                end
            end

            %ftem = '../../data/mosart/MOSART_global_8th_20180211c.nc';
            fmos = sprintf('%s/MOSART_%s_%s.nc','./inputdata',usrdat_name,datestr(now, 'cyymmdd'));
            fdom = sprintf('%s/domain_%s_%s.nc','./inputdata',usrdat_name,datestr(now, 'cyymmdd'));

            if ~exist(fmos,'file')
                generate_mosart_from_drt(drt,ftemp,fmos,fdom,0);
            end

        elseif strcmp(res{i},'8th') || strcmp(res{i},'half')
        [iout, icon] = find_mosart_cell(ftemp,xout,yout,Abasin);
        in = [iout; icon];
        
        % Generate MOSARt input file
        fmos = CreateMOSARTUgridInputForE3SM2(in, ftemp, './inputdata', usrdat_name);

        if strcmp(res{i},'half')
        % Generate ELM surface dataset
        felm = CreateCLMUgridSurfdatForE3SM(in,ftemp2, './inputdata', usrdat_name, ...
               [],[],[],[],[],[],[],[],[],[],[],[],[],[]);
        end
        % Generate lnd domain file
        xc = ncread(fmos, 'longxy'); xv = zeros(4,length(xc));     
        yc = ncread(fmos, 'latixy'); yv = zeros(4,length(xc));
        if exist(['Channel_geometry_DRT_' basin '_' res{i} '.mat'],'file')
            load(['Channel_geometry_DRT_' basin '_' res{i} '.mat']);
        else
            ID = ncread(fmos,'ID'); dnID = ncread(fmos,'dnID');
            area = ncread(fmos,'area');
            [rwid,rdep,flood_2yr] = get_geometry(xc,yc,ID,dnID,area);
    
            save(['Channel_geometry_DRT_' basin '_' res{i} '.mat'],'rwid','rdep','flood_2yr');
        end
        ncwrite(fmos,'rwid',rwid);
        ncwrite(fmos,'rdep',rdep);
        ncwrite(fmos,'rwid0',5.*rwid);

        xv(1,:) = xc - dx/2; xv(2,:) = xc + dx/2; 
        xv(3,:) = xc + dx/2; xv(4,:) = xc - dx/2; 
        yv(1,:) = yc - dx/2; yv(2,:) = yc - dx/2; 
        yv(3,:) = yc + dx/2; yv(4,:) = yc + dx/2; 
        frac = ncread(fmos, 'frac');
        mask = ones(length(frac),1);

        fdom = sprintf('%s/domain_lnd_%s_%s.nc','./inputdata',usrdat_name,datestr(now,'cyymmdd'));
        area  = generate_lnd_domain(xc,yc,xv,yv,frac,mask,[],fdom);

        end
        
        % Convert the domain file to SCRIP format
        fout = sprintf('%s/domain_lnd_%s_SCRIP_%s.nc','./inputdata',usrdat_name,datestr(now,'cyymmdd'));
        convert_domain_to_SCRIPgrid(fdom,fout);
        convert_domain_to_SCRIPgrid('./inputdata/mosart_susquehanna_domain_mpas.nc', ...
                                    './inputdata/mosart_susquehanna_domain_mpas_SCRIP.nc');
        if debug 
            % Show river newwork
            longxy = ncread(fmos,'longxy');
            latixy = ncread(fmos,'latixy');
            figure;
            show_river_network(fmos,0);hold on;
            plot(longxy,latixy,'k.'); 
            title(basin,'FontSize',15,'FontWeight','bold');
            % Show river geometry
            rwid = ncread(fmos,'rwid');
            rdep = ncread(fmos,'rdep');
            figure; set(gcf,'Position',[10 10 1200 400]);
            subplot(2,2,1);
            patch(xv,yv,rwid,'LineStyle','none'); colorbar;
            title('DRT Bankfull width [m]','FontSize',15,'FontWeight','bold');
            subplot(2,2,2);
            patch(xv,yv,rdep,'LineStyle','none'); colorbar;
            title('DRT Bankfull depth [m]','FontSize',15,'FontWeight','bold');
            
            xv2 = ncread('./inputdata/mosart_susquehanna_domain_mpas.nc','xv');
            yv2 = ncread('./inputdata/mosart_susquehanna_domain_mpas.nc','yv');
            [ni,nj,nv] = size(xv2);
            xv2 = reshape(xv2,[ni,nv])';
            yv2 = reshape(yv2,[ni,nv])';
            rwid2 = ncread('./inputdata/mosart_susquehanna_parameter_mpas.nc','rwid');
            rdep2 = ncread('./inputdata/mosart_susquehanna_parameter_mpas.nc','rdep');
            subplot(2,2,3);
            patch_variable_mesh(xv2,yv2,rwid2); colorbar;
            title('MPAS Bankfull width [m]','FontSize',15,'FontWeight','bold');
            subplot(2,2,4);
            patch_variable_mesh(xv2,yv2,rdep2); colorbar;
            title('MPAS Bankfull depth [m]','FontSize',15,'FontWeight','bold');
        end
        
    end
end

function [fdir,flen,facc] = download_DRT(wg)
    if ~exist('./tmp/','dir')
        mkdir('./tmp/');
    end
    % Download flow direction
    fname = 'DRT_16th_FDR_globe.asc';
    fdir  = ['./tmp/' fname];
    if ~exist('./tmp/DRT_16th_FDR_globe.asc','file')
        url = 'http://files.ntsg.umt.edu/data/DRT/upscaled_global_hydrography/by_HydroSHEDS_Hydro1k/flow_direction/';
        cmd   = [wg ' -O ' fdir ' ' url fname]; 
    end
    if ~exist(fdir,'file')
        [status,cmdout] = system(cmd,'-echo');
    end
    if exist(fdir,'file')
        disp('DRT 16th flow DIR file downloads suscessfully!');
    else
        disp(['Cannot download ' fname ' from ' url]);
    end
    
    % Download flow length
    fname = 'DRT_16th_FDISTANCE_globe.asc';
    flen  = ['./tmp/' fname];
    if ~exist('./tmp/DRT_16th_FDISTANCE_globe.asc','file')
        url = 'http://files.ntsg.umt.edu/data/DRT/upscaled_global_hydrography/by_HydroSHEDS_Hydro1k/flow_distance/';
        cmd   = [wg ' -O ' flen ' ' url fname]; 
    end
    if ~exist(flen,'file')
        [status,cmdout] = system(cmd,'-echo');
    end
    if exist(flen,'file')
        disp('DRT 16th flow DISTANCE file downloads suscessfully!');
    else
        disp(['Cannot download ' fname ' from ' url]);
    end
    
    % Download flow accumulation
    fname = 'DRT_16th_SourceArea_globe_float.asc';%'DRT_16th_FDISTANCE_globe.asc';
    facc  = ['./tmp/' fname];
    if ~exist('./tmp/DRT_16th_SourceArea_globe_float.asc','file')
        url = 'http://files.ntsg.umt.edu/data/DRT/upscaled_global_hydrography/by_HydroSHEDS_Hydro1k/upstream_drainagearea/';
        cmd   = [wg ' -O ' facc ' ' url fname]; 
    end
    if ~exist(facc,'file')
        [status,cmdout] = system(cmd,'-echo');
    end
    if exist(facc,'file')
        disp('DRT 16th flow ACCUMULATION file downloads suscessfully!');
    else
        disp(['Cannot download ' fname ' from ' url]);
    end
    
end

function [ftemp, ftemp2] = download_temp(res,wg)
    fdir  = '../../data/mosart/';
    url   = 'https://web.lcrc.anl.gov/public/e3sm/inputdata/rof/mosart/';
    if strcmp(res,'half')
        fname  = 'MOSART_Global_half_20210422.nc';
        ftemp  = [fdir fname];
        cmd    = [wg ' -O ' ftemp ' ' url fname]; 

        fname2 = 'surfdata_0.5x0.5_simyr2010_c200624.nc';
        url2   = 'https://web.lcrc.anl.gov/public/e3sm/inputdata/lnd/clm2/surfdata_map/';
        ftemp2 = [fdir fname2];
        cmd2   = [wg ' -O ' ftemp2 ' ' url2 fname2]; 

        if ~exist(ftemp,'file')
            [status,cmdout] = system(cmd,'-echo');
        end
        if exist(ftemp,'file')
            disp('Template MOSART input file downloads suscessfully!');
        else
            disp(['Cannot download ' fname ' from ' url]);
        end

        if ~exist(ftemp2,'file')
            [status2,cmdout2] = system(cmd2,'-echo');
        end
        if exist(ftemp2,'file')
            disp('Template ELM surface data downloads suscessfully!');
        else
            disp(['Cannot download ' fname2 ' from ' url2]);
        end

    elseif strcmp(res,'8th')
        fname = 'MOSART_global_8th_20180211c.nc';
        ftemp = [fdir fname];
        cmd   = [wg ' -O ' ftemp ' ' url fname]; 
        if ~exist(ftemp,'file')
            [status,cmdout] = system(cmd,'-echo');
        end
        if exist(ftemp,'file')
            disp('Template MOSART input file downloads suscessfully!');
        else
            disp(['Cannot download ' fname ' from ' url]);
        end

        ftemp2 = [];
    else
        error('Only support for half and 8th resolution now!');
    end
end
