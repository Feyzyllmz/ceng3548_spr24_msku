import json
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk


light_blue = '#87CEFA'
navy_blue = '#000080'

with open('/home/feyza/Desktop/CENG/Second-Term/Web Mining/formula1/teams.json', 'r') as file:
    team_data = json.load(file)
    if team_data:
        team_names = [team['full_team_name'] for team in team_data]
        championships = [int(team['world_championships']) for team in team_data]

        sorted_data = sorted(zip(team_names, championships), key=lambda x: x[1], reverse=True)  
        sorted_names, sorted_championships = zip(*sorted_data)
        
        cmap = plt.cm.Blues(np.linspace(1, 0, len(sorted_championships)))  
        cmap[0] = matplotlib.colors.to_rgba(navy_blue, alpha=1.0) 
        cmap[-1] = matplotlib.colors.to_rgba(light_blue, alpha=1.0)  

        fig, ax = plt.subplots(figsize=(10, 6)) 
        bars = ax.bar(sorted_names, sorted_championships, color=cmap)  
        ax.set_ylabel('WORLD CHAMPIONSHIPS')
        ax.set_xlabel('TEAMS')
        ax.set_title('F1 TEAMS')
        ax.tick_params(axis='x', rotation=90)  

        sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues, norm=plt.Normalize(vmin=min(sorted_championships), vmax=max(sorted_championships)))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label('World Championships')

        plt.tight_layout()
        plt.savefig("teams_chart.png")
        plt.show()
