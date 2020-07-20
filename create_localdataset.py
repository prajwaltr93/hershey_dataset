#!/home/starkm42/opencvprjcts/bin/python3

#filename : create_localdataset.py
#author : PRAJWAL T R
#date last modified : Mon Jul 13 14:25:12 2020
#comments :





breaks = [0, 100, 600, 900, 1200, 1569]
for break_ind in range(len(breaks) - 1):
    for _, _, filelist in walk(traverse_path):
        for file in filelist[breaks[break_ind] : breaks[break_ind + 1]]:
