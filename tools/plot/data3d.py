import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm
from matplotlib.animation import FuncAnimation

# Load the JSON data from the file
with open('sesh.json') as f:
    data = json.load(f)

# Convert timestamp to integer if necessary
for i in range(len(data)):
    if type(data[i]['Timestamp'][0]) != int:
        data[i]['Timestamp'][0] = int(data[i]['Timestamp'][0])

# Extract data from the JSON into separate lists
timestamps = [i['Timestamp'][0] for i in data]
temperatures = [i['Temperature'][0] for i in data]
moistures = [i['Moisture'][0] for i in data]
lights = [i['Light'][0] for i in data] 
conductivities = [i['Conductivity'][0] for i in data]

# Define the number of steps to forecast
n_steps = 5

# Fit the ARIMA model to the temperature data
model = sm.tsa.ARIMA(temperatures, order=(1, 1, 1))
model_fit = model.fit()
predictions_temperature = model_fit.predict(start=len(temperatures), end=len(temperatures)+n_steps-1)

# Convert the predicted timestamps to the same format as the original timestamps
predicted_timestamps = [timestamps[-1] + (i+1)*300 for i in range(n_steps)]

# Concatenate the original temperature data and the predicted temperature values
all_temperatures = temperatures + list(predictions_temperature)

# Create a 3D subplot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('dimgray')

# Plot the temperature, moisture, and conductivity data
sc1 = ax.scatter(timestamps, temperatures, moistures, c=conductivities, cmap='viridis', marker='o', label='Moisture')
sc2 = ax.scatter(timestamps, temperatures, lights, c=conductivities, cmap='viridis', marker='o', label='Light')
sc3 = ax.scatter(timestamps, temperatures, conductivities, c=conductivities, cmap='viridis', marker='o', label='Conductivity')

# Plot the predicted temperature values
sc4 = ax.scatter(predicted_timestamps, predictions_temperature, [moistures[-1]]*n_steps, c='r', marker='o', label='Temperature Predictions')

# Add labels to the x, y, and z axes
ax.set_xlabel("Timestamp")
ax.set_ylabel("Temperature")
ax.set_zlabel("Sensor Value")

# Add a legend
ax.legend()

# Change the title of the window
fig.suptitle("Sensor Data")

# Define the update function for the animation
def update(frame):
    ax.view_init(elev=10, azim=frame)
    return sc1, sc2, sc3, sc4,

# Create and start the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=120)

# Show the plot
plt.show()