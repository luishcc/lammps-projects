import numpy as np
import os

from write import DataFile
from readLammps import DumpReader

class Point:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

class Atoms:
    def __init__(self, points, density):
        self.number = len(points)
        self.positions = points
        self.density = density
        return

class Box:
    def __init__(self, lx, ly, lz):
        self.xlo = -lx/2.
        self.xhi = lx/2.
        self.ylo = -ly/2.
        self.yhi = ly/2.
        self.zlo = 0
        self.zhi = lz

def perturbation_radius(amp, length, z):
    return 1 + amp * np.cos((2 * np.pi * z) / length)


def remove_atoms(list, a, wl):
    i = 0
    id_to_remove = []
    for atom in list:
        i+=1
        print(i, len(list))
        x, y, z = atom.x
        max_dist = radius*perturbation_radius(a, wl, z)
        current_dist = np.sqrt(x**2 + y**2)
        print(current_dist, max_dist)
        if current_dist > max_dist:
            id_to_remove.append(atom.id)

    for i in sorted(id_to_remove, reverse=True):
        del list[i]


density = 6.9
radius = 6.0
wave_number = 0.15
wave_length = (2 * np.pi * radius) / wave_number
perturbation_amp = 0.03 * radius

box = Box(6*radius, 6*radius, wave_length)

data = DumpReader('dump.atom')
remove_atoms(data.atoms, perturbation_amp, wave_length)

positions = []
for atom in data.atoms:
    positions.append(Point(atom.x))

atoms_list = Atoms(positions, 1.)

data = DataFile(box, atoms_list)
data.write_file('perturbed', os.getcwd())
