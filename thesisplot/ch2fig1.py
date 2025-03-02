import numpy as np
import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 15,
    'figure.figsize': (1.7*side, .7*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def eos_warren(a, b, rho, rd=0.75, kbT=1):
  alpha = 0.101
  c = 4.16
  d = 18
  t2 = alpha*a*rho**2
  t3 = 2*alpha*b*rd**4 * (rho**3 - c*rho**2 + d)
  return rho*kbT + t2  + t3


def eos_jamali(a, b, rho, rd=0.75, kbT=1, paper=True):
  alpha = 0.101
  c = 4.63
  d = 7.55
  t2 = alpha*a*rho**2
  # t3 = 2*alpha*b*rd**4*(rho**3-c*rho**2+d*rho) #From the paper; wrong?
  t3 = 2*alpha*b*rd**4*(rho**3 - c*rho**2 + d * (rho**paper) )
  t4 = (alpha*b*rd**4*rho**2) / (np.sqrt(abs(a)))
  return rho*kbT + t2  + t3 - t4


density = np.linspace(0, 15, 100)

fig, (ax, ax1) = plt.subplots(1,2, sharey=True)

fig.subplots_adjust(wspace=.03)

marker = ['k^', 'bs', 'go', 'y+']
i = 0
for a in np.linspace(-40, -70, 2):
  for b in np.linspace(20, 35, 2):
    # plt.plot(density, [eos_warren(a,25,r) for r in density], 'k-', label = a)
    ax.plot(density, [eos_jamali(a,b,r, rd=0.75) for r in density], marker[i], 
             label = rf'A={a}, B={b}', markerfacecolor='none')
    ax1.plot(density, [eos_jamali(a,b,r, rd=0.65) for r in density], marker[i], 
             label = rf'A={a}, B={b}', markerfacecolor='none')
    i+=1
    # plt.plot(density, [eos_jamali(a,25,r, paper=False) for r in density], 'r-.', label = a)

ax.set_ylim(-300, 400)
ax1.set_ylim(-300, 400)

ax.set_xlabel(r'$\rho$')
ax1.set_xlabel(r'$\rho$')

ax.set_ylabel(r'$p$')

ax.legend(loc='lower right', frameon=False)
ax.plot([min(density), max(density)], [0, 0], 'k--')
ax.annotate(r'$r_d=0.75$', xy=(2, -200), fontsize=15)

ax1.legend(loc='upper left', frameon=False)
ax1.plot([min(density), max(density)], [0, 0], 'k--')
ax1.annotate(r'$r_d=0.65$', xy=(2, 50), fontsize=15)

plt.tight_layout()

fig.savefig('ch2fig1.pdf', dpi = dpi)
# plt.show()
