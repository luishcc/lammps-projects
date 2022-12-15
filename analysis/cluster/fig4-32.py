import numpy as np




################################################################################
################################################################################

# a = [50,60,70,80,85,90]
a = [.538, .380, .311, 0.206, 0.230, 0.266, .321, .451, .704, .901, 1.137]; xlabel = '$Oh$'

# normal avg
# Different peaks
b = [.074, .160, .285, .406, .380, .296, .215, .210, .196, .135, .130] # sat/main

# Break_avg
# Different peaks
b = [.069, .180, .276, .411, .389, .282, .213, .200, .183, .126, .133] # sat/main

b_var = [.00, .00, 00, .004, .006, .0053, .0026, .0039, .0057, .0025, .0056]


wave = [.1, .1, .1,
.011887547350585061, .01338236354459586,
.018927425365090515, .017959188701441885, .016553644129911244,
.014737153310297676, .013920311412504544, .01340404171055144]

radii = [2, 4, 6, 10, 8, 6, 6, 6, 6, 6, 6]
radii = [r*0.8 for r in radii]

wavelen = [1/i for i in wave]
red_wavenum = [i*2*np.pi*r for i,r in zip(wave,radii)]


lt = [.277, .277, .277, .250, .250, .250, .210, .181, .158, .148, .139]

lv = [.581, .581, .581, .426, .426, .426, .617, 1.224, 2.97, 4.87, 7.75]
# lv = [4.8/i for i in lv]

rho = [6.95, 6.95, 6.95, 7.65, 7.65, 7.65, 8.30, 8.95, 9.6, 9.92, 10.24]
lr = [np.cbrt(1/i) for i in rho]


q_var = [0, 0, 0,
3.990705611232144e-06,
2.408162556723014e-06,
3.156327982930347e-06,
2.328394395880221e-06,
1.8893985765694086e-06,
2.054396275751638e-06,
3.954677744054939e-06,
9.193559899539904e-06]
# q_var = [i*2*np.pi*r*0.8 for i,r in zip(q_var,radii)]



# a = wavelen ; xlabel = '$\lambda$'
# a = red_wavenum ; xlabel = '$\chi$'
# a = lv ; xlabel = '$L_v$'
# a = lt ; xlabel = '$L_t$'
# a = lr ; xlabel = '$L_r$'
# a = radii ; xlabel = '$R_0$'

# a = [1/i**2 for i in a] ; xlabel = '$Oh^{-2}$'

# a = [(i/j) for i, j in zip(lt, lv)]; xlabel = '$L_v/L_T$'
# a = [(i/j) for i, j in zip(lr, lv)]; xlabel = '$L_r/L_T$'
# a = [r/(i) for i,r in zip(lt,radii)]; xlabel = '$R_0/L_T$'
# a = [r/(i) for i,r in zip(lv,radii)]; xlabel = '$R_0/L_v$'
# a = [r/(i) for i,r in zip(lr,radii)]; xlabel = '$R_0/L_r$'


# a = [r**2/(i*j) for r, i, j in zip(radii, lv, lt)]; xlabel = '$R_0^{2}/L_vL_T$'
# a = [(r**2/(i*j))**0.25 for r, i, j in zip(radii, lv, lt)]; xlabel = '$R_0/\sqrt{L_vL_T}$'
a = [(r**3/(i*j*p))**0.333 for r, i, j, p in zip(radii, lv, lt, lr)]; xlabel = '$R_0/\sqrt[3]{L_vL_TL_r}$'
# a = [(r*x**2/(i*j*p))**0.25 for r, x, i, j, p in zip(radii, wavelen, lv, lt, lr)]; xlabel = '$R_0/\sqrt[3]{L_vL_TL_r}$'
# a = [((j/i)/x) for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$L_v/\lambda L_T$'
# a = [((j/i)*x) for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$\lambda L_v/ L_T$'
# a = [(x**2/(i*j))**0.5 for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$\lambda^2/ L_v L_T$'
# a = [(x) for x, i, j in zip(wave, lv, lt)] ; xlabel = '$1/\lambda $'
# a = [x*(i/j) for x, i, j in zip(red_wavenum, lv, lt)] ; xlabel = '$\chi L_T/L_v$'
# a = [(r*p)/(i*j) for r,p,  i, j in zip(radii,  lr, lv, lt)] ; xlabel = '$RL_T/L_pL_v$'
# a = [x/i for x, i in zip(wave, lv)] ; xlabel = '$L_v/\lambda$'
# a = [r/x for x, r in zip(wave, radii)]; xlabel = '$R_0/\chi$'


scale = (max(a) - min(a)) * 0.2
lla = min(a)
ula = max(a)
a2 = np.linspace(lla-scale, ula+scale, 100)

fit = np.polyfit(a,b, 1)
b_fit = [fit[0]*i + fit[1] for i in a2 ]

fit2 = np.polyfit(a, b, 2)
b_fit2 = [fit2[0]*i**2 + fit2[1]*i +fit2[2] for i in a2 ]

def ff2(a):
    return fit2[0]*a**2 + fit2[1]*a +fit2[2]

def ff1(a):
    return fit[0]*a + fit[1]

def fexp(x,a,b):
    return a*np.exp(x*b)

def fpow(x,a,b):
    return a*x**b

from scipy.optimize import curve_fit
pars, cov = curve_fit(f=fexp, xdata=a, ydata=b, p0=[0, 0], bounds=(-np.inf, np.inf))
pars2, cov2 = curve_fit(f=fpow, xdata=a, ydata=b, p0=[0, 0], bounds=(-np.inf, np.inf))

stdevs = np.sqrt(np.diag(cov))
stdevs2 = np.sqrt(np.diag(cov2))

s1 = 0
s2 = 0
s3 = 0
s4 = 0
for i, j in enumerate(a):
    print(i,j)
    s1 += (ff1(j)-b[i])**2
    s2 += (ff2(j)-b[i])**2
    s3 += (fexp(j, *pars)-b[i])**2
    s4 += (fpow(j, *pars2)-b[i])**2

print(s1, s2, s3, s4)
print(fit, '\n', fit2)
print(pars, stdevs)
print(pars2, stdevs2)


import matplotlib as mpl
from matplotlib import container


dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (1.1*side, 1.1*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt

fig, axs = plt.subplots(ncols=1, nrows=1)
# gs = axs[0, 0].get_gridspec()
# for ax in axs[0, :]:
#     ax.remove()
# axbig = fig.add_subplot(gs[0, :])


# fig.tight_layout()

ax2 = axs


ax2.plot(a2, b_fit, 'k--', label='Linear fit')
# ax2.plot(a2, b_fit2, 'k--', label='Quadratic fit')
# ax2.plot(a2, fexp(a2, *pars), 'b--', label='exp fit')
# ax2.plot(a2, fpow(a2, *pars2), 'k--', label='$y=0.13x^{-0.5}$')
# ax2.plot(a, b, 'ko', label='Simulation')
ax2.errorbar(a, b, xerr = np.sqrt(q_var)*2*np.pi*4.8, yerr = np.sqrt(b_var),
fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
handles, labels = ax2.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax2.legend(handles, labels, loc='upper left', ncol=1)
ax2.set_ylabel('$N_{satellite}/N_{total}$')
ax2.set_xlabel(xlabel)
# ax2.set_xlabel(r'$3R_0/l_T$')



# plt.savefig('fig4.pdf', bbox_inches='tight', dpi=dpi )


plt.show()
