

clear

yst = 1975;
yed = 2099;

delta_gmt = 0.5:0.5:3
gmt_regrid = load('Y:\experiment\timing_us\result\gmt_regrid.txt');

id = [1:97]

rcp26 = [5 9 12 18 26 30 33 37 41 45 51 55 61 67 73 77 81 85 88 91 94]
rcp45 = [1 3 6 10 13 16 19 22 24 27 31 34 38 42 46 49 50 52 56 59 62 65 68 71 74 78 82 86 89 92 95]
rcp60 = [7 14 20 28 35 39 43 47 53 57 63 69 75 79 83 96]
rcp85 = [2 4 8 11 15 17 21 23 25 29 32 36 40 44 48 54 58 60 64 66 70 72 76 80 84 87 90 93 97]


indir1 = ['D:\work\experiments\vic_columbia\vic_columbia\']
indir2 = ['D:\work\experiments\columbia_cmip5\data\routed_streamflow\']
indir3 = ['D:\work\experiments\columbia_cmip5\data\routed_streamflow\streamflow_vic4.1.2_hist_ncar_day.csv\historical_maurer02\streamflow_vic4.1.2_hist_ncar_day.csv']
indir4 = ['D:\work\experiments\correct_PDF\data\BPA\Nat\']

site_1 = {'PRIRA','DALLE','BROWN','GCOUL','ARROW'}
site_2 = {'PRIES','DALLE','BROWN','GCOUL','ARROW'}
site_3 = {'PRD','TDA','BRN','GCL','ARD'}
col = [15 18 20 50 6]
col_3 = [141 170 28 73 11]

bpa_date = load('D:\work\experiments\correct_PDF\data\BPA\Nat\date.txt');
bpa = xlsread([indir4,'NRNI_Flows_1928-2008_Corrected_03-2015.csv']); 

for num=1:5
        
    gcm = xlsread([indir2,'streamflow_cmip5_ncar_day_',cell2mat(site_2(num)),'.csv\cmip5\cmip5_ncar_day\streamflow_cmip5_ncar_day_',cell2mat(site_2(num)),'.csv'],['streamflow_cmip5_ncar_day_',cell2mat(site_2(num))]); 
        
    %read data 
    for k=1:length(id)             
        runoff_base(num,k,:) = gcm(gcm(:,1)>=1975 & gcm(:,1)<=2004,id(k)+3);
        runoff_future(num,k,:) = gcm(gcm(:,1)>=2070 & gcm(:,1)<=2099,id(k)+3);
        for i=yst:yed              
            qmean(k,i-yst+1) = nanmean(gcm(gcm(:,1)==i,id(k)+3));
            qmedian(k,i-yst+1) = nanmedian(gcm(gcm(:,1)==i,id(k)+3));
            q95(k,i-yst+1) = quantile(gcm(gcm(:,1)==i,id(k)+3),0.95);
            q5(k,i-yst+1) = quantile(gcm(gcm(:,1)==i,id(k)+3),0.05);        
        end
    end
    
    % calculate the timing of significant changes in distribution    
    for i=1:length(id)          
        qmean_base(num,i,:) = qmean(i,1:30);
        qmean_future(num,i,:) = qmean(i,96:125);
        
        qmedian_base(num,i,:) = qmedian(i,1:30);
        qmedian_future(num,i,:) = qmedian(i,96:125);
        
        q5_base(num,i,:) = q5(i,1:30);
        q5_future(num,i,:) = q5(i,96:125);
        
        q95_base(num,i,:) = q95(i,1:30);
        q95_future(num,i,:) = q95(i,96:125);                     
    end
    
    bpa_raw(num,:) = bpa(bpa_date(:,3)>=1975 & bpa_date(:,3)<=2004,col_3(num));
    for i=1975:2004          
        bpa_ave(num,i-yst+1) = nanmean(bpa(bpa_date(:,3)==i,col_3(num)));
        bpa_med(num,i-yst+1) = nanmedian(bpa(bpa_date(:,3)==i,col_3(num)));
        bpa_95(num,i-yst+1) = quantile(bpa(bpa_date(:,3)==i,col_3(num)),0.95);
        bpa_5(num,i-yst+1) = quantile(bpa(bpa_date(:,3)==i,col_3(num)),0.05);
    end    
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% save
data = bpa_raw(1,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_raw_daily_BPA_HIST.txt data
data = bpa_raw(2,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_raw_daily_BPA_HIST.txt data
data = bpa_raw(3,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_raw_daily_BPA_HIST.txt data
data = bpa_raw(4,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_raw_daily_BPA_HIST.txt data
data = bpa_raw(5,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_raw_daily_BPA_HIST.txt data

data = bpa_ave(1,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_Qmean_BPA_HIST.txt data
data = bpa_ave(2,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_Qmean_BPA_HIST.txt data
data = bpa_ave(3,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_Qmean_BPA_HIST.txt data
data = bpa_ave(4,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_Qmean_BPA_HIST.txt data
data = bpa_ave(5,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_Qmean_BPA_HIST.txt data

data = bpa_med(1,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_Qmedian_BPA_HIST.txt data
data = bpa_med(2,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_Qmedian_BPA_HIST.txt data
data = bpa_med(3,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_Qmedian_BPA_HIST.txt data
data = bpa_med(4,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_Qmedian_BPA_HIST.txt data
data = bpa_med(5,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_Qmedian_BPA_HIST.txt data

data = bpa_5(1,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_Q5_BPA_HIST.txt data
data = bpa_5(2,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_Q5_BPA_HIST.txt data
data = bpa_5(3,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_Q5_BPA_HIST.txt data
data = bpa_5(4,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_Q5_BPA_HIST.txt data
data = bpa_5(5,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_Q5_BPA_HIST.txt data

data = bpa_95(1,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_Q95_BPA_HIST.txt data
data = bpa_95(2,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_Q95_BPA_HIST.txt data
data = bpa_95(3,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_Q95_BPA_HIST.txt data
data = bpa_95(4,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_Q95_BPA_HIST.txt data
data = bpa_95(5,:)';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_Q95_BPA_HIST.txt data


%%%%%%%%%%%%%%%%%%% raw GCM data
data = squeeze(nanmean(runoff_base(1,[13 15],:),2));
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_raw_daily_CCSM4_HIST.txt data
clear data
data = squeeze(runoff_future(1,13:16,:))';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_raw_daily_CCSM4_RCPs.txt data
clear data

data = squeeze(nanmean(runoff_base(2,[13 15],:),2));
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_raw_daily_CCSM4_HIST.txt data
clear data
data = squeeze(runoff_future(2,13:16,:))';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_raw_daily_CCSM4_RCPs.txt data
clear data

data = squeeze(nanmean(runoff_base(3,[13 15],:),2));
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_raw_daily_CCSM4_HIST.txt data
clear data
data = squeeze(runoff_future(3,13:16,:))';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_raw_daily_CCSM4_RCPs.txt data
clear data

data = squeeze(nanmean(runoff_base(4,[13 15],:),2));
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_raw_daily_CCSM4_HIST.txt data
clear data
data = squeeze(runoff_future(4,13:16,:))';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_raw_daily_CCSM4_RCPs.txt data
clear data

data = squeeze(nanmean(runoff_base(5,[13 15],:),2));
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_raw_daily_CCSM4_HIST.txt data
clear data
data = squeeze(runoff_future(5,13:16,:))';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_raw_daily_CCSM4_RCPs.txt data
clear data



%%%%%%%%%%%%%%%%%%%%%%% CGM metrics
% Qmean
data(1,:) = squeeze(nanmean(qmean_base(1,[13 15],:),2));
data(2:5,:) = squeeze(qmean_future(1,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_Qmean_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(qmean_base(2,[13 15],:),2));
data(2:5,:) = squeeze(qmean_future(2,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_Qmean_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(qmean_base(3,[13 15],:),2));
data(2:5,:) = squeeze(qmean_future(3,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_Qmean_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(qmean_base(4,[13 15],:),2));
data(2:5,:) = squeeze(qmean_future(4,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_Qmean_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(qmean_base(5,[13 15],:),2));
data(2:5,:) = squeeze(qmean_future(5,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_Qmean_CCSM4.txt data
clear data

% qmedian
data(1,:) = squeeze(nanmean(qmedian_base(1,[13 15],:),2));
data(2:5,:) = squeeze(qmedian_future(1,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_Qmedian_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(qmedian_base(2,[13 15],:),2));
data(2:5,:) = squeeze(qmedian_future(2,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_Qmedian_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(qmedian_base(3,[13 15],:),2));
data(2:5,:) = squeeze(qmedian_future(3,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_Qmedian_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(qmedian_base(4,[13 15],:),2));
data(2:5,:) = squeeze(qmedian_future(4,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_Qmedian_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(qmedian_base(5,[13 15],:),2));
data(2:5,:) = squeeze(qmedian_future(5,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_Qmedian_CCSM4.txt data
clear data

% q5
data(1,:) = squeeze(nanmean(q5_base(1,[13 15],:),2));
data(2:5,:) = squeeze(q5_future(1,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_Q5_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(q5_base(2,[13 15],:),2));
data(2:5,:) = squeeze(q5_future(2,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_Q5_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(q5_base(3,[13 15],:),2));
data(2:5,:) = squeeze(q5_future(3,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_Q5_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(q5_base(4,[13 15],:),2));
data(2:5,:) = squeeze(q5_future(4,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_Q5_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(q5_base(5,[13 15],:),2));
data(2:5,:) = squeeze(q5_future(5,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_Q5_CCSM4.txt data
clear data

% q95
data(1,:) = squeeze(nanmean(q95_base(1,[13 15],:),2));
data(2:5,:) = squeeze(q95_future(1,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\PRIES_Q95_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(q95_base(2,[13 15],:),2));
data(2:5,:) = squeeze(q95_future(2,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\DALLE_Q95_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(q95_base(3,[13 15],:),2));
data(2:5,:) = squeeze(q95_future(3,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\BROWN_Q95_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(q95_base(4,[13 15],:),2));
data(2:5,:) = squeeze(q95_future(4,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\GCOUL_Q95_CCSM4.txt data
clear data

data(1,:) = squeeze(nanmean(q95_base(5,[13 15],:),2));
data(2:5,:) = squeeze(q95_future(5,13:16,:));
data = data';
save -ascii D:\work\experiments\correct_PDF\ana\result\ARROW_Q95_CCSM4.txt data
clear data



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% plot
% Qmean
figure
for num=1:length(site_1) 
    
    subplot(2,3,num)       
    % future  
    for i=1:length(rcp45)
        sdata = sort(squeeze(qmean_future(num,rcp45(i),:)));
        myqmean_future_rcp45(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'g-','Color',[0.8 0.8 1],'linewidth',0.2);
        hold on   
    end  
    for i=1:length(rcp85)
        sdata = sort(squeeze(qmean_future(num,rcp85(i),:)));
        myqmean_future_rcp85(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'r-','Color',[1 0.8 0.8],'linewidth',0.2);
        hold on   
    end   
        
    % base
    for i=1:97
        sdata = sort(squeeze(qmean_base(num,i,:)));
        myqmean_base(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'k-','color', [0.83 0.82 0.78],'linewidth',0.2);
        hold on   
    end
    xlabel('Year')
    ylabel('CDF')
    title('Qmean (cfs)')    
    
    % CCSM4
    % base
    data = squeeze(qmean_base(num,:,:)); % CCSM4
    sdata = sort(nanmean(data([13 15],:)));
    plot(sdata,(0.5:length(sdata))./length(sdata),'k--','linewidth',1);
    hold on 
    % rcp45
    data = squeeze(qmean_future(num,13,:)); % CCSM4
    sdata = sort(data);
    plot(sdata,(0.5:length(sdata))./length(sdata),'b--','linewidth',1);
    hold on    
    % rcp85
    data = squeeze(qmean_future(num,15,:)); % CCSM4
    sdata = sort(data);
    plot(sdata,(0.5:length(sdata))./length(sdata),'r--','linewidth',1);
    hold on     
    
    % ensemble mean
    % base
    sdata = nanmean(myqmean_base);
    plot(sdata,(0.5:length(sdata))./length(sdata),'k-','linewidth',2);
    hold on 
    % rcp45
    sdata = nanmean(myqmean_future_rcp45);
    plot(sdata,(0.5:length(sdata))./length(sdata),'b-','linewidth',2);
    hold on    
    % rcp85
    sdata = nanmean(myqmean_future_rcp85);
    plot(sdata,(0.5:length(sdata))./length(sdata),'r-','linewidth',2);
    hold on    
    
    xlabel('Qmean (cfs)')
    ylabel('CDF')
    title(cell2mat(site_1(num)))
end


% qmedian
figure
for num=1:length(site_1) 
    
    subplot(2,3,num)       
    % future  
    for i=1:length(rcp45)
        sdata = sort(squeeze(qmedian_future(num,rcp45(i),:)));
        myqmedian_future_rcp45(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'g-','Color',[0.8 0.8 1],'linewidth',0.2);
        hold on   
    end  
    for i=1:length(rcp85)
        sdata = sort(squeeze(qmedian_future(num,rcp85(i),:)));
        myqmedian_future_rcp85(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'r-','Color',[1 0.8 0.8],'linewidth',0.2);
        hold on   
    end   
        
    % base
    for i=1:97
        sdata = sort(squeeze(qmedian_base(num,i,:)));
        myqmedian_base(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'k-','color', [0.83 0.82 0.78],'linewidth',0.2);
        hold on   
    end
    xlabel('Year')
    ylabel('CDF')
    title('qmedian (cfs)')    
    
    % CCSM4
    % base
    data = squeeze(qmedian_base(num,:,:)); % CCSM4
    sdata = sort(nanmean(data([13 15],:)));
    plot(sdata,(0.5:length(sdata))./length(sdata),'k--','linewidth',1);
    hold on 
    % rcp45
    data = squeeze(qmedian_future(num,13,:)); % CCSM4
    sdata = sort(data);
    plot(sdata,(0.5:length(sdata))./length(sdata),'b--','linewidth',1);
    hold on    
    % rcp85
    data = squeeze(qmedian_future(num,15,:)); % CCSM4
    sdata = sort(data);
    plot(sdata,(0.5:length(sdata))./length(sdata),'r--','linewidth',1);
    hold on     
    
    % ensemble mean
    % base
    sdata = nanmean(myqmedian_base);
    plot(sdata,(0.5:length(sdata))./length(sdata),'k-','linewidth',2);
    hold on 
    % rcp45
    sdata = nanmean(myqmedian_future_rcp45);
    plot(sdata,(0.5:length(sdata))./length(sdata),'b-','linewidth',2);
    hold on    
    % rcp85
    sdata = nanmean(myqmedian_future_rcp85);
    plot(sdata,(0.5:length(sdata))./length(sdata),'r-','linewidth',2);
    hold on    
    
    xlabel('qmedian (cfs)')
    ylabel('CDF')
    title(cell2mat(site_1(num)))
end


% q5
figure
for num=1:length(site_1) 
    
    subplot(2,3,num)       
    % future  
    for i=1:length(rcp45)
        sdata = sort(squeeze(q5_future(num,rcp45(i),:)));
        myq5_future_rcp45(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'g-','Color',[0.8 0.8 1],'linewidth',0.2);
        hold on   
    end  
    for i=1:length(rcp85)
        sdata = sort(squeeze(q5_future(num,rcp85(i),:)));
        myq5_future_rcp85(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'r-','Color',[1 0.8 0.8],'linewidth',0.2);
        hold on   
    end   
        
    % base
    for i=1:97
        sdata = sort(squeeze(q5_base(num,i,:)));
        myq5_base(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'k-','color', [0.83 0.82 0.78],'linewidth',0.2);
        hold on   
    end
    xlabel('Year')
    ylabel('CDF')
    title('q5 (cfs)')    
    
    % CCSM4
    % base
    data = squeeze(q5_base(num,:,:)); % CCSM4
    sdata = sort(nanmean(data([13 15],:)));
    plot(sdata,(0.5:length(sdata))./length(sdata),'k--','linewidth',1);
    hold on 
    % rcp45
    data = squeeze(q5_future(num,13,:)); % CCSM4
    sdata = sort(data);
    plot(sdata,(0.5:length(sdata))./length(sdata),'b--','linewidth',1);
    hold on    
    % rcp85
    data = squeeze(q5_future(num,15,:)); % CCSM4
    sdata = sort(data);
    plot(sdata,(0.5:length(sdata))./length(sdata),'r--','linewidth',1);
    hold on     
    
    % ensemble mean
    % base
    sdata = nanmean(myq5_base);
    plot(sdata,(0.5:length(sdata))./length(sdata),'k-','linewidth',2);
    hold on 
    % rcp45
    sdata = nanmean(myq5_future_rcp45);
    plot(sdata,(0.5:length(sdata))./length(sdata),'b-','linewidth',2);
    hold on    
    % rcp85
    sdata = nanmean(myq5_future_rcp85);
    plot(sdata,(0.5:length(sdata))./length(sdata),'r-','linewidth',2);
    hold on    
    
    xlabel('q5 (cfs)')
    ylabel('CDF')
    title(cell2mat(site_1(num)))
end


% q95
figure
for num=1:length(site_1) 
    
    subplot(2,3,num)       
    % future  
    for i=1:length(rcp45)
        sdata = sort(squeeze(q95_future(num,rcp45(i),:)));
        myq95_future_rcp45(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'g-','Color',[0.8 0.8 1],'linewidth',0.2);
        hold on   
    end  
    for i=1:length(rcp85)
        sdata = sort(squeeze(q95_future(num,rcp85(i),:)));
        myq95_future_rcp85(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'r-','Color',[1 0.8 0.8],'linewidth',0.2);
        hold on   
    end   
        
    % base
    for i=1:97
        sdata = sort(squeeze(q95_base(num,i,:)));
        myq95_base(i,:) = sdata;
        plot(sdata,(0.5:length(sdata))./length(sdata),'k-','color', [0.83 0.82 0.78],'linewidth',0.2);
        hold on   
    end
    xlabel('Year')
    ylabel('CDF')
    title('q95 (cfs)')    
    
    % CCSM4
    % base
    data = squeeze(q95_base(num,:,:)); % CCSM4
    sdata = sort(nanmean(data([13 15],:)));
    plot(sdata,(0.5:length(sdata))./length(sdata),'k--','linewidth',1);
    hold on 
    % rcp45
    data = squeeze(q95_future(num,13,:)); % CCSM4
    sdata = sort(data);
    plot(sdata,(0.5:length(sdata))./length(sdata),'b--','linewidth',1);
    hold on    
    % rcp85
    data = squeeze(q95_future(num,15,:)); % CCSM4
    sdata = sort(data);
    plot(sdata,(0.5:length(sdata))./length(sdata),'r--','linewidth',1);
    hold on     
    
    % ensemble mean
    % base
    sdata = nanmean(myq95_base);
    plot(sdata,(0.5:length(sdata))./length(sdata),'k-','linewidth',2);
    hold on 
    % rcp45
    sdata = nanmean(myq95_future_rcp45);
    plot(sdata,(0.5:length(sdata))./length(sdata),'b-','linewidth',2);
    hold on    
    % rcp85
    sdata = nanmean(myq95_future_rcp85);
    plot(sdata,(0.5:length(sdata))./length(sdata),'r-','linewidth',2);
    hold on    
    
    xlabel('q95 (cfs)')
    ylabel('CDF')
    title(cell2mat(site_1(num)))
end


    