import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat


R = 10
ratio = 6
sim_case = f'R{R}_ratio{ratio}_A50'

path_to_data = os.getcwd()
dir = '/'.join([path_to_data, sim_case])

dir_out = '/'.join([dir, 'fig'])

if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

snap = 0
file = dir + f'/{snap}.dat'
while os.path.isfile(file):
    print(file)
    data = read_dat(file)

    plt.figure(1)

    for i in range(1, len(data)):
        plt.plot(data['dz'], data[str(i-1)],  label=f'R={i}')

    plt.xlabel(r'$\delta z$')
    plt.ylabel(r'$G(r,\delta z)$')
    plt.ylim(-0.05, 1.1)
    plt.plot([0, data['dz'][-1]], [0, 0], 'k--')
    plt.legend(loc='right')
    plt.savefig(f'{dir_out}/{snap}.png', format='png')
    plt.close(1)
    snap += 1
    file = dir + f'/{snap}.dat'
