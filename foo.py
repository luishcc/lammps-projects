import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')

u = np.linspace(0, 2*np.pi, 1000)
v = np.linspace(0, 2*np.pi, 1000)
U, V = np.meshgrid(u, v)

A = 4
X = U
Y1 = (np.cos(U)+A)*np.cos(V)
Z1 = (np.cos(U)+A)*np.sin(V)


#Y2 = (U + 3)*np.cos(V)
#Z2 = (U + 3)*np.sin(V)

ax.plot_surface(X, Y1, Z1)
#ax.plot_surface(X, Y1, Z1, alpha=0.3, color='red', rstride=6, cstride=12)
#ax.plot_surface(X, Y2, Z2, alpha=0.3, color='blue', rstride=6, cstride=12)
plt.show()
