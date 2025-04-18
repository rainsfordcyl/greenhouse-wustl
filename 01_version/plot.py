import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Ensure the 'plot' folder exists (create it if needed)
if not os.path.exists('plot'):
    os.makedirs('plot')

# Read data from the CSV file in the 'data' folder
df = pd.read_csv('data/sensor_log.csv', parse_dates=['datetime'])

# Plot datetime vs. raw_value
plt.plot(df['datetime'], df['raw_value'])

# Optionally format the x-axis for dates to ensure ticks are readable
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gcf().autofmt_xdate()  # rotates and aligns the tick labels nicely

# Label and title
plt.xlabel('Datetime')
plt.ylabel('Raw Value')
plt.title('Datetime vs. Raw Value')

# Save the plot into the 'plot' folder
plt.savefig('plot/sensor_datetime_vs_raw_value.png', dpi=300, bbox_inches='tight')