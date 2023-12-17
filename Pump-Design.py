import numpy as np
import matplotlib.pyplot as plt


# Initialize parameters
rho_water = 1000  # Density of water (kg/m^3)
g = 9.81  # Acceleration due to gravity (m/s^2)
tank_height = 5  # Tank height (m)
piston_diameter = 1  # Piston diameter (m)
valve_diameter = 0.1  # Valve diameter (m)
high_tide_height = 3  # High tide height (m)
tidal_cycle_duration = 43200  # Tidal cycle duration in seconds (12 hours)
p_atm = 1E5 # Atmospheric pressure

# Tidal simulation (simplified)
def simulate_tide_flow(duration, high_tide_height):
    # Generate a sinusoidal pattern for tide simulation
    t = np.linspace(0, duration, 1000)
    tide_height = high_tide_height * np.sin(2 * np.pi * t / duration)
    pressure = p_atm - rho_water * g * tide_height
    velocity = np.sqrt(2 * ((pressure - p_atm) / rho_water))
    return t, tide_height, velocity

# Solving for tide height and velocity
t, tide_height, velocity = simulate_tide_flow(tidal_cycle_duration, high_tide_height)

"""
The following code uses real data for an average day during the month of August in Los Angeles.
"""

# Adjusted flow velocity calculation to handle negative tide heights
def adjusted_flow_velocity(height):
    # If height is negative, set flow velocity to 0
    if height < 0:
        return 0
    else:
        # Calculate flow velocity using Bernoulli's equation
        pressure = rho_water * g * height
        return np.sqrt(2 * g * height)

# Calculate adjusted flow velocities for each tide height
adjusted_flow_velocities = np.array([adjusted_flow_velocity(h) for h in tide_height])

# Re-plotting tide height and flow velocity with adjusted values
fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Tide Height (m)', color=color)
ax1.plot(t, tide_height, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_ylabel('Flow Velocity (m/s)', color=color)
ax2.plot(t, adjusted_flow_velocities, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Tide Height and Flow Velocity Over Time')
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load the tide data file
file_path = 'C:/Users/jhwit/Documents/GitHub/SENECA/tide_data.csv'
tide_data = pd.read_csv(file_path)

# Convert tide height from feet to meters (1 foot = 0.3048 meters)
tide_data['Verified (m)'] = tide_data['Verified (ft)'] * 0.3048

# Combine date and time columns and convert to datetime
tide_data['Datetime'] = pd.to_datetime(tide_data['Date'] + ' ' + tide_data['Time (GMT)'])

# Adjusted flow velocity calculation to handle negative tide heights
def adjusted_flow_velocity(height):
    if height < 0:
        return 0
    else:
        return np.sqrt(2 * 9.81 * height)

# Filter data for the month of August
august_data = tide_data[tide_data['Datetime'].dt.month == 8]

# Group by time of day and calculate the average tide height for each time
august_data['Time of Day'] = august_data['Datetime'].dt.time
average_august_tides = august_data.groupby('Time of Day')['Verified (m)'].mean()

# Calculate average flow velocity for each time of day in August
average_august_velocities = average_august_tides.apply(adjusted_flow_velocity)

# Convert 'Time of Day' to a datetime object for plotting
times = pd.to_datetime(average_august_tides.index.astype(str))

# Convert time to hours for plotting
hours = times.hour + times.minute / 60 + times.second / 3600

# Plotting both average tide height and average flow velocity for an average day in August
plt.figure(figsize=(12, 6))
plt.plot(hours, average_august_tides, label='Average Tide Height (m)', color='tab:blue')
plt.plot(hours, average_august_velocities, label='Average Flow Velocity (m/s)', color='tab:red')
plt.xlabel('Time of Day (Hours)')
plt.ylabel('Average Tide Height (m) / Average Flow Velocity (m/s)')
plt.title('Average Tide Height and Flow Velocity Over an Average Day in August (Los Angeles)')
plt.xticks(np.arange(0, 25, 1))
plt.grid(True)
plt.legend()
plt.show()
