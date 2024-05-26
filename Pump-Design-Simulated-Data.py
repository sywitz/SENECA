import numpy as np
import matplotlib.pyplot as plt

# Initialize parameters
rho_water = 1000  # Density of water (kg/m^3)
g = 9.81  # Acceleration due to gravity (m/s^2)
high_tide_height = 3  # High tide height (m)
tidal_cycle_duration = 43200  # Tidal cycle duration in seconds (12 hours)
p_atm = 1E5 # Atmospheric pressure

# Define the number of seconds in 24 hours
seconds_in_day = 24 * 60 * 60

# Sinusoidal tide simulation and velocity function
def simulate_tide(duration, high_tide_height):
    # Time array over 24 hours
    t = np.linspace(0, duration, 1000)
    
    # Convert time to hours for plotting
    t_hours = t / 3600

    # Sinusoidal tide height
    tide_height = high_tide_height * np.sin(2 * np.pi * t / duration) + 3

    # Calculate the slope of the tide height to determine v_in and v_out
    tide_slope = np.gradient(tide_height, t)

    # v_in is the slope of tide when tide is rising (positive slope)
    # v_out is the absolute value of the slope when tide is falling (negative slope)
    v_in = np.where(tide_slope > 0, tide_slope, 0)
    v_out = np.where(tide_slope < 0, -tide_slope, 0)

    return t_hours, tide_height, v_in, v_out

# Simulate and plot the corrected velocities over a 24 hour period
t_hours, tide_height, v_in, v_out = simulate_tide(seconds_in_day, high_tide_height)

# Create the plot with time in hours
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot the tide height
ax1.plot(t_hours, tide_height, label='Tide Height (m)', color='tab:blue')
ax1.set_xlabel('Time (Hours)')
ax1.set_ylabel('Tide Height (m)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a secondary y-axis for the velocities
ax2 = ax1.twinx()
ax2.plot(t_hours, v_in, label='Intake Velocity (v_in)', color='tab:green')
ax2.plot(t_hours, v_out, label='Outtake Velocity (v_out)', color='tab:red')
ax2.set_ylabel('Velocity (m/s)', color='tab:gray')
ax2.tick_params(axis='y', labelcolor='tab:gray')

# Add legends and title
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title('Tide Height, Intake Velocity, and Outtake Velocity Over a 24-Hour Period')

# Show the plot with time in hours
plt.show()

"""
The following code uses real data for an average day during the month of August in Los Angeles.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load the tide data file
file_path = 'C:/Users/jhwit/Documents/GitHub/SENECA/tide_data.csv'
tide_data_la = pd.read_csv(file_path)

# Convert 'Date' and 'Time (GMT)' to a single datetime object and convert tide height to meters
tide_data_la['Datetime'] = pd.to_datetime(tide_data_la['Date'] + ' ' + tide_data_la['Time (GMT)'])
tide_data_la['Verified (m)'] = tide_data_la['Verified (ft)'] * 0.3048  # Convert feet to meters

# Calculate the slope of the tide height over time to determine v_in and v_out
tide_data_la['Slope'] = np.gradient(tide_data_la['Verified (m)'], edge_order=2)

# v_in is the positive slope, v_out is the negative slope
tide_data_la['v_in'] = np.where(tide_data_la['Slope'] > 0, tide_data_la['Slope'], 0)
tide_data_la['v_out'] = np.where(tide_data_la['Slope'] < 0, -tide_data_la['Slope'], 0)

# Convert Datetime to hours from the start of the day for plotting
tide_data_la['Hours'] = (tide_data_la['Datetime'] - tide_data_la['Datetime'].min()).dt.total_seconds() / 3600.0

# Ensure that x-axis ticks represent each hour of the day
num_hours = 24
hour_ticks = np.arange(0, num_hours, 1)  # Generate a range of numbers from 0 to 23 representing each hour

# Calculate the area of the valve in square meters
valve_area = np.pi * (valve_diameter / 2)**2

# Calculate flow rate in m³/s for v_in and v_out separately and convert to GPM
tide_data_la['Flow Rate in (GPM)'] = valve_area * tide_data_la['v_in'] * 15850.3
tide_data_la['Flow Rate out (GPM)'] = valve_area * tide_data_la['v_out'] * 15850.3

# Plotting the data
fig, ax1 = plt.subplots(figsize=(14, 7))

# Tide Height
ax1.plot(tide_data_la['Hours'], tide_data_la['Verified (m)'], label='Tide Height (m)', color='tab:blue')
ax1.set_xlabel('Time (Hours)')
ax1.set_ylabel('Tide Height (m)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_xticks(hour_ticks)  # Set the x-axis to have ticks at each hour
ax1.set_xlim(0, num_hours)  # Set the limit of the x-axis to be from 0 to 24 hours

# Flow Rates in GPM
ax2 = ax1.twinx()
ax2.plot(tide_data_la['Hours'], tide_data_la['Flow Rate in (GPM)'], label='Flow Rate In (GPM)', color='tab:green')
ax2.plot(tide_data_la['Hours'], tide_data_la['Flow Rate out (GPM)'], label='Flow Rate Out (GPM)', color='tab:red')
ax2.set_ylabel('Flow Rate (GPM)', color='tab:gray')
ax2.tick_params(axis='y', labelcolor='tab:gray')

# Adjust secondary y-axis to make room for the flow rate labels
ax2.spines["right"].set_position(("outward", 60))

# Add legends and title
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title('Tide Height and Flow Rate Over a 24-Hour Period')
plt.show()