import re
import matplotlib.pyplot as plt
import numpy as np

def process_pressure_data(pressure_string):
    # Extract numeric values using regular expression
    match = re.match(r'(\d+)/(\d+) mmHg', pressure_string)
    
    if match:
        systolic, diastolic = map(int, match.groups())
        return systolic, diastolic
    else:
        raise ValueError("Invalid pressure string format")
def pressure_bar(days, pressure_data):
    # Example pressure data for each day
    # days = [1,  3]  # Updated to represent days as numbers
    # pressure_data = ["120/80 mmHg",  "115/75 mmHg"]

    # Process the pressure data for each day
    processed_data = [process_pressure_data(pressure) for pressure in pressure_data]

    # Extract systolic and diastolic values
    systolic_values, diastolic_values = zip(*processed_data)

    # Calculate the average systolic and diastolic values
    average_systolic = np.mean(systolic_values)
    average_diastolic = np.mean(diastolic_values)

    # Set a smaller figure size
    plt.figure(figsize=(8, 6))

    # Plotting the data
    bar_width = 0.35
    index = range(len(days))

    plt.bar(index, systolic_values, bar_width, label='Systolic Pressure')
    plt.bar([i + bar_width for i in index], diastolic_values, bar_width, label='Diastolic Pressure')

    # Add reference line for average pressure
    plt.axhline(y=average_systolic, color='green', linestyle='--', label=f'Average Systolic ({average_systolic:.2f})')
    plt.axhline(y=average_diastolic, color='orange', linestyle='--', label=f'Average Diastolic ({average_diastolic:.2f})')

    plt.xlabel('Days of Month')
    plt.ylabel('Pressure (mmHg)')
    plt.title('Systolic and Diastolic Pressure for Each Day')
    plt.xticks([i + bar_width / 2 for i in index], days)
    plt.legend()

    # Adjust the position of the legend
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.show()
