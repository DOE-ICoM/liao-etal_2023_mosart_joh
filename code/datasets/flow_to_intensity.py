mm2m = 0.001 #units m/mm

dFlow = 0.2 #units m3/s

sRunoff = 0.0001  #mm/s

dArea = 1E6 #m2
dTime_step = 86400 #s

#mass in one day
dRunoff_mass = sRunoff * mm2m * dArea * dTime_step
print(dRunoff_mass) #m3

dFlow = dRunoff_mass / dTime_step #m3/sec

print(dFlow)

dFlow_mm = dFlow / (mm2m * dArea) #mm/s
print(dFlow_mm)