import json
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk

light_blue = '#87CEFA'
navy_blue = '#000080'

with open('/home/feyza/Desktop/CENG/Second-Term/Web Mining/formula1/drivers.json', 'r') as file:
    driver_data = json.load(file)
    if driver_data:
        names = [f"{driver['first_name']} {driver['last_name']}" for driver in driver_data]
        points = [float(driver['points']) for driver in driver_data]

        sorted_data = sorted(zip(names, points), key=lambda x: x[1])
        sorted_names, sorted_points = zip(*sorted_data)
        
        cmap = plt.cm.Blues(np.linspace(0, 1, len(sorted_points)))  
        cmap[0] = matplotlib.colors.to_rgba(light_blue, alpha=1.0)  
        cmap[-1] = matplotlib.colors.to_rgba(navy_blue, alpha=1.0)  

        fig, ax = plt.subplots(figsize=(10, 6))  
        bars = ax.bar(sorted_names, sorted_points, color=cmap)  
        ax.set_ylabel('POINTS')
        ax.set_xlabel('DRIVERS')
        ax.set_title('F1 DRIVERS')
        ax.tick_params(axis='x', rotation=90) 

        sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues, norm=plt.Normalize(vmin=min(sorted_points), vmax=max(sorted_points)))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label('Points')

        plt.tight_layout()
        plt.savefig("drivers_chart.png")
        plt.show()
