import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, colors

# Constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
M = 5.972e24  # Mass of Earth (kg)
R = 6371e3  # Radius of Earth (m)
h0 = 200e3  # Initial height of spacecraft (m)
v0 = 7500  # Initial velocity of spacecraft (m/s)
dt = 0.1  # Time step (s)
t_max = 1500  # Maximum simulation time (s)
theta = np.pi / 4  # Entry angle
specific_heat = 1000  # Specific heat capacity of the spacecraft material (J/kg/K)
mass = 1000  # Mass of the spacecraft (kg)
surface_area = 20  # Surface area of the spacecraft (m^2)

# Function to compute atmospheric density
def atmospheric_density(h):
    return 1.225 * np.exp(-h / 8200)

# Function to compute temperature rise due to atmospheric friction
def temperature_rise(v, rho):
    return (0.5 * rho * v**3) / (specific_heat * mass)

# Initialize arrays
t_values = np.arange(0, t_max, dt)
h_values = np.zeros_like(t_values)
v_values = np.zeros_like(t_values)
temp_values = np.zeros_like(t_values)
h_values[0] = h0
v_values[0] = v0
temp_values[0] = 300  # Initial temperature of the spacecraft surface

# Simulation loop
for i in range(1, len(t_values)):
    h = h_values[i-1]
    v = v_values[i-1]
    rho = atmospheric_density(h)
    a_gravity = -G * M / (R + h)**2
    a_drag = -0.5 * rho * v**2 * surface_area / mass  # Drag
    a_total = a_gravity + a_drag
    h_values[i] = h + v * np.sin(theta) * dt
    v_values[i] = v + a_total * dt
    temp_values[i] = temp_values[i-1] + temperature_rise(v, rho) * dt

# Convert height to kilometers
h_values /= 1000

# Scale temperature by 1000
temp_values /= 1000

# Create custom colormap inspired by reentry colors
colors_list = ['#0000ff', '#00ffff', '#80ff00', '#ffff00', '#ff8000', '#ff0000']
cmap_reentry = colors.LinearSegmentedColormap.from_list('reentry', colors_list)

# Normalize temperature values
norm = colors.Normalize(vmin=temp_values.min(), vmax=temp_values.max())

# 3D Visualization of trajectory with changing color
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(h_values * np.cos(theta), h_values * np.sin(theta), t_values, c=temp_values, cmap=cmap_reentry, norm=norm, label='Temperature (x1000 K)')
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Time (s)')
ax.set_title('3D Trajectory of Spacecraft Reentry')
ax.legend()
fig.colorbar(sc, label='Temperature (x1000 K)')
plt.show()
