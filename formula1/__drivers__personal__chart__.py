import json
import matplotlib.pyplot as plt

with open('/home/feyza/Desktop/CENG/Second-Term/Web Mining/formula1/result_drivers_personal_infos.json', 'r') as file:
    result_drivers = json.load(file)
    drivers = list(set(d["driver"] for d in result_drivers))

    for driver in drivers:
        driver_data = [d for d in result_drivers if d["driver"] == driver]
        driver_name = driver.split()[0] + "_" + driver.split()[1]
        driver_results = []
        grand_prix = []
        
        for result in driver_data:
            driver_results.append(int(result["pts"]))
            grand_prix.append(result["grand_prix"])

        plt.figure(figsize=(10, 6))
        plt.plot(grand_prix, driver_results, marker='o')
        plt.title(driver.upper())
        plt.xlabel("GRAND PRIX")
        plt.ylabel("PTS")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        
        plt.savefig(driver_name + "_chart.png")

        plt.show()
