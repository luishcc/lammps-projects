import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


file = 'log.lammps'

gamma = []

i=0
flag = True
with open(file, 'r') as fd:
    for _ in range(30):
        fd.readline()
    while flag:
        print(i)
        i+=1
        line = fd.readline()
        print(line)
        try:
            a = line.split()[0]
        except:
            if i>=1000:
                break
            continue
        if a == 'v_gamma':
            print('TRUE')
            while True:
                try:
                    line = fd.readline().split()
                    gamma.append(float(line[0]))
                except:
                    flag = False
                    break
        if i>=1000:
            break

print(sum(gamma)/len(gamma))
