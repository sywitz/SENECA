"""
The following code uses real data for an average day during the month of August in Los Angeles.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize parameters
rho_water = 1000  # Density of water (kg/m^3)
g = 9.81  # Acceleration due to gravity (m/s^2)
p_atm = 1E5 # Atmospheric pressure
tank_height = 3  # Tank height (m)
piston_diameter = 1  # Piston diameter (m)
head_bouyancy = 9402*g # Total possible head bouyancy (N)
valve_diameter = 0.058  # Valve diameter (m)
gasket_force = 20 # Normal force between gasket and tank walls (N)
friction_coef = 1 # Coefficient of friction between rubber and steel https://structx.com/Material_Properties_005a.html
friction_force = gasket_force*friction_coef

# Calculating piston head mass for steel-clad concrete
piston_head_volume = 2.41 # Piston and Head volume (m^3)
density_concrete = 2400 # Density of conrete (kg/m^3)
density_steel = 7850 # Density of galvanized steel (kg/m^3)
piston_head_mass =  2.41*(0.9*2400 + 0.1*7850) # Piston and Head mass (7097.45 kg)

# Force applied by the tides acting on the head, will be used for power calculations
piston_force = piston_head_mass*g - friction_force

# Load the tide data file
file_path = 'C:/Users/jhwit/Documents/GitHub/SENECA/Numerical-Sims/tide_data.csv'
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

# Calculate the area of the piston in square meters
piston_area = np.pi * (piston_diameter / 2)**2
print(piston_area)
print(piston_force)

# Calculate flow rate in m³/s for v_in and v_out separately and convert to GPM
tide_data_la['Flow Rate in (GPM)'] = piston_area * tide_data_la['v_in'] * 15850.3
tide_data_la['Flow Rate out (GPM)'] = piston_area * tide_data_la['v_out'] * 15850.3

# Calculate the power as the product of piston force and change in height
tide_data_la['Power (W)'] = piston_force * tide_data_la['Slope']
tide_data_la['Abs Power (W)'] = abs(tide_data_la['Power (W)'])  # Absolute value of power

# Calculate the power as the product of piston force and change in height
tide_data_la['Power (kW)'] = np.abs(piston_force * tide_data_la['Slope']) / 1000  # Convert to kW

# Calculate the average power (in kW) over the whole time period
average_power = tide_data_la['Power (kW)'].mean()

# Calculate the average GPM for inflow and outflow
average_gpm_in = tide_data_la['Flow Rate in (GPM)'].mean()
average_gpm_out = tide_data_la['Flow Rate out (GPM)'].mean()

# Calculate the total energy generated (in kWh) over the whole time period
time_period_hours = num_hours  # Assuming the data covers a full 24-hour period
total_energy_generated = average_power * time_period_hours

# Print the average power and total energy generated
print(f"Average Power: {average_power:.2f} kW")
print(f"Total Energy Generated: {total_energy_generated:.2f} kWh")
print(f"Average GPM in: {average_gpm_in:.2f} GPM")
print(f"Average GPM out: {average_gpm_out:.2f} GPM")

# Calculate the total volume generated in the tank (in gallons) for inflow and outflow
total_volume_in = tide_data_la['Flow Rate in (GPM)'].sum() / 60  # Convert GPM to gallons per second
total_volume_out = tide_data_la['Flow Rate out (GPM)'].sum() / 60  # Convert GPM to gallons per second

# Assuming 24 hours in a day
total_volume_in_day = total_volume_in * 3600 * 24  # Convert gallons per second to gallons per day
total_volume_out_day = total_volume_out * 3600 * 24  # Convert gallons per second to gallons per day

# Print the total volume generated in the tank for inflow and outflow per day
print(f"Total Volume In (per day): {total_volume_in_day:.2f} gallons")
print(f"Total Volume Out (per day): {total_volume_out_day:.2f} gallons")

# Plotting Tide Height and Flow Rate
fig, ax1 = plt.subplots(figsize=(14, 7))

# Tide Height
ax1.plot(tide_data_la['Hours'], tide_data_la['Verified (m)'], label='Tide Height (m)', color='tab:blue')
ax1.set_xlabel('Time (Hours)')
ax1.set_ylabel('Tide Height (m)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_xticks(hour_ticks)  # Set the x-axis to have ticks at each hour
ax1.set_xlim(0, num_hours)  # Set the limit of the x-axis to be from 0 to 24 hours

# Flow Rates in GPM (with adjusted scale)
ax2 = ax1.twinx()
ax2.plot(tide_data_la['Hours'], tide_data_la['Flow Rate in (GPM)'], label='Flow Rate In (GPM)', color='tab:green')
ax2.plot(tide_data_la['Hours'], tide_data_la['Flow Rate out (GPM)'], label='Flow Rate Out (GPM)', color='tab:red')
ax2.set_ylabel('Flow Rate (GPM)', color='tab:gray')
ax2.tick_params(axis='y', labelcolor='tab:gray')
ax2.spines['right'].set_position(('outward', 40))  # Adjust position for the second y-axis
ax2.set_ylim(0, max(tide_data_la['Flow Rate in (GPM)'].max(), tide_data_la['Flow Rate out (GPM)'].max()) + 1)

# Add legends and title
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title('Tide Height and Flow Rate Over a 24-Hour Period')

# Show the first plot
plt.show()

# Create a separate plot for Tide Height and Power
fig, ax1 = plt.subplots(figsize=(14, 7))

# Tide Height
ax1.plot(tide_data_la['Hours'], tide_data_la['Verified (m)'], label='Tide Height (m)', color='tab:blue')
ax1.set_xlabel('Time (Hours)')
ax1.set_ylabel('Tide Height (m)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_xticks(hour_ticks)  # Set the x-axis to have ticks at each hour
ax1.set_xlim(0, num_hours)  # Set the limit of the x-axis to be from 0 to 24 hours

# Power (in kW)
ax2 = ax1.twinx()
ax2.spines['right'].set_position(('outward', 40))  # Adjust position for the second y-axis
ax2.plot(tide_data_la['Hours'], tide_data_la['Power (kW)'], label='Power (kW)', color='tab:purple')
ax2.set_ylabel('Power (kW)', color='tab:purple')
ax2.tick_params(axis='y', labelcolor='tab:purple')

# Add legends and title
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title('Tide Height and Power (kW) Over a 24-Hour Period')

# Show the second plot
plt.show()