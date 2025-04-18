import os
import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
csv_file = 'data/history/0418_sensor_log.csv'

# Read the CSV, parsing the 'datetime' column
df = pd.read_csv(csv_file, parse_dates=['datetime'])

# Specify the sensor ID you want to plot
sensor_id = 0  # Change this value to the desired sensor ID

# Filter for the specified sensor_id from the CSV data
df_sensor = df[df['sensor_id'] == sensor_id]

# Create the plot with the sensor ID included in the title
plt.figure(figsize=(10, 6))
plt.plot(df_sensor['datetime'], df_sensor['percent'])
plt.xlabel('Datetime')
plt.ylabel('Percent')
plt.title(f'Sensor {sensor_id}: Percent vs. Time')
plt.xticks(rotation=45)
plt.tight_layout()

# Prepare output directory and filename including sensor_id in the filename
plot_dir = 'plot'
os.makedirs(plot_dir, exist_ok=True)
base_name = os.path.splitext(os.path.basename(csv_file))[0]
plot_filename = f"{base_name}_sensor{sensor_id}.png"
plot_path = os.path.join(plot_dir, plot_filename)

# Save the figure and display the plot
plt.savefig(plot_path)
plt.show()