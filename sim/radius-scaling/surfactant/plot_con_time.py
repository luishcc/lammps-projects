import os
import numpy as np
import matplotlib.pyplot as plt 


def run_snapshot(dir, time):
    # Read surface concentration from .dat file
    with open(f'{dir}/surface_concentration/{time}.dat') as fd:
        line = fd.readline()
        line = line.split(' ')
        num = int(line[4].split('=')[1])
        dz = float(line[3].split('=')[1])
        con_s = np.zeros(num)
        for line in fd:
            line = line.split(' ')
            id = int(line[0])
            value = float(line[1])
            con_s[id] = value
    # Read bulk concentration from .dat file
    with open(f'{dir}/bulk_concentration/{time}.dat') as fd:
        line = fd.readline()
        line = line.split(' ')
        num = int(line[4].split('=')[1])
        con_b = np.zeros(num)
        for line in fd:
            line = line.split(' ')
            id = int(line[0])
            value = float(line[1])
            con_b[id] = value
    # Read surface profile radius from .dat file
    with open(f'{dir}/surface_profile/{time}.dat') as fd:
        line = fd.readline().split(' ')
        dz = float(line[5].split('=')[1])
        num = int(line[6].split('=')[1])
        shape = np.ones(num)*-1
        for id, line in enumerate(fd):
            line = line.split(' ')
            radius = float(line[1])
            shape[id] = radius  
    
    # vol = np.pi*shape**2*dz
    area = 2*np.pi*shape*dz
    
    return shape, con_s/area/4, con_b/area/4, dz

def get_breaktime(dir):
    with open(f'{dir}/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())-1
    return snap

def read_sim(dir, num_snaps):

    shape = []
    bulk = []
    surface = []

    breaktime = get_breaktime(dir)

    for t in range(breaktime, breaktime-num_snaps, -1):
        h, cons, conb, dz = run_snapshot(dir, t)
        shape.append(h)
        bulk.append(conb)
        surface.append(cons)

    shape = np.array(shape)
    conb = np.array(bulk)
    cons = np.array(surface)   
    
    dist = shape[0].argmin() - int(len(shape[0])/2)
    shape = np.roll(shape, -dist, axis=1)
    conb = np.roll(conb, -dist, axis=1)
    cons = np.roll(cons, -dist, axis=1)

    flip = shape[0].argmin() - shape[0].argmax() > 0
    if flip:
        shape = np.flip(shape, axis=1)
        conb = np.flip(conb, axis=1)
        cons = np.flip(cons, axis=1) 

    return shape, conb, cons 

def findNumSnaps(path, n):
    times = []
    for i in range(n):
        dir = f'{path}/{i+1}'
        times.append(get_breaktime(dir))
    return min(times)

##############################

sc = 2.9
path = f'/home/luishcc/hdd/radius_scaling/surfactant/{sc}'

num_sim = 20
num_snaps = findNumSnaps(path, num_sim)

shapes = []
bulks = []
surfaces = []

for i in range(num_sim):
    dir = f'{path}/{i+1}'
    
    shape, bulk, surface = read_sim(dir, num_snaps)    
 
    shapes.append(shape)
    bulks.append(bulk)
    surfaces.append(surface)



# ids = np.linspace(0.5,len(shapes[0])+0.5, len(shapes[0]))*dz
ids = np.linspace(-.5,.5, len(shapes[0][0]))


import matplotlib as mpl
dpi = 1600
side = 7
fontsize = 24
rc_fonts = {
    "font.family": "serif",
    "font.size": fontsize,
    'figure.figsize': (0.8*side, .7*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)
import matplotlib.animation as animation


# fig, (ax, ax2) = plt.subplots(2,1, sharex=True)
# fig, ax = plt.subplots(1,1)
# fig2, ax2 = plt.subplots(1,1)


sum = np.zeros(np.shape(shapes[0]))
sumsq = np.zeros(np.shape(shapes[0]))
for shape in shapes:
    sum += shape
    sumsq += shape**2
    # ax.plot(ids, shape, 'c--')

avg = sum/num_sim
var = sumsq/num_sim - avg**2
std = np.sqrt(var)

sum = np.zeros(np.shape(shapes[0]))
sumsq = np.zeros(np.shape(shapes[0]))
for con in surfaces:
    sum += con
    sumsq += con**2
    # ax.plot(ids, shape, 'c--')
avg2 = sum/num_sim
var = sumsq/num_sim - avg2**2
std2 = np.sqrt(var)

sum = np.zeros(np.shape(shapes[0]))
sumsq = np.zeros(np.shape(shapes[0]))
for con in bulks:
    sum += con
    sumsq += con**2
    # ax.plot(ids, shape, 'c--')
avgb = sum/num_sim
var = sumsq/num_sim - avgb**2
stdb = np.sqrt(var)



class PauseAnimation:
    def __init__(self, shape, std, conb, stdb, cons, stds):
        
        fig, (ax, ax2) = plt.subplots(2,1, sharex=True)
        self.ax = ax
        self.ax2 = ax2

        self.cons = cons
        self.conb = conb
        self.stdb = stdb
        self.stds = stds

        self.line = ax.plot(ids, shape[-1], 'k-', label=f'Snapshot = 0')[0]
        self.line2 = ax.plot(ids, -shape[-1], 'k-')[0]
        self.poly = ax.fill_between(ids, shape[-1]-std[-1], shape[-1]+std[-1], color='gray', alpha = 0.4)
        self.poly2 = ax.fill_between(ids, -shape[-1]-std[-1], -shape[-1]+std[-1], color='gray', alpha = 0.4)
        ax.set(ylim=[-18, 18], xlabel='z', ylabel='h')
        # ax.set_aspect('equal', adjustable='box')
        self.legend = ax.legend(loc='upper left', frameon=False)

        self.l1 = ax2.plot(ids, conb[-1], 'b-', label=f'Snapshot = 0')[0]
        self.p1 = ax2.fill_between(ids, conb[-1]-stdb[-1], conb[-1]+stdb[-1], color='lightblue', alpha = 0.6)

        self.l2 = ax2.plot(ids, cons[-1], 'k-')[0]
        self.p2 = ax2.fill_between(ids, cons[-1]-stds[-1], cons[-1]+stds[-1], color='gray', alpha = 0.4)
        
        ax2.set(ylim=[0, 2.5], xlabel='z', ylabel=r'$\Gamma$')
        ax2.plot([-0.5, 0.5], [1.75, 1.75], 'r--')
               
        self.animation = animation.FuncAnimation(
            fig, self.update, frames=len(shape), interval=2, blit=True)
        self.paused = False

        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused

    def update(self, frame):
        # for each frame, update the data stored on each artist.
        h = shape[-frame]
        st = std[-frame]
        self.line.set_ydata(h)
        self.line2.set_ydata(-h)

        dummy = self.ax.fill_between(ids, h-st, h+st)
        vert = dummy.get_paths()[0]
        dummy.remove()
        self.poly.set_paths([vert.vertices])

        dummy = self.ax.fill_between(ids, -h-st, -h+st)
        vert = dummy.get_paths()[0]
        dummy.remove()
        self.poly2.set_paths([vert.vertices])

        ss = self.cons[-frame]
        bb = self.conb[-frame]
        self.l1.set_ydata(bb)
        self.l2.set_ydata(ss)

        st = self.stds[-frame]
        dummy = self.ax2.fill_between(ids, ss-st, ss+st)
        vert = dummy.get_paths()[0]
        dummy.remove()
        self.p2.set_paths([vert.vertices])

        st = self.stdb[-frame]
        dummy = self.ax2.fill_between(ids, bb-st, bb+st)
        vert = dummy.get_paths()[0]
        dummy.remove()
        self.p1.set_paths([vert.vertices])

        self.legend.get_texts()[0].set_text(f'Snapshot = {frame}') 
       
        return (self.line, self.line2, self.poly, self.poly2, self.l1, self.l2, self.p1, self.p2, self.legend)
    
        
    
pa = PauseAnimation(avg, std, avgb, stdb, avg2, std2)
plt.show()

    