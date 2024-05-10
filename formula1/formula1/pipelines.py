import json

from itemadapter import ItemAdapter

from formula1.items import Driver



""" class Formula1Pipeline:
    def open_spider(self, spider):
        self.file_drivers = open("drivers.json", "w")
        self.file_drivers.write("[\n")  
        self.drivers = []

    def close_spider(self, spider):
        driver_lines = [
            "\t" + json.dumps(ItemAdapter(p).asdict())
            for p in self.drivers
        ]
        drivers_lines_joined = ",\n".join(driver_lines)
        self.file_drivers.write(drivers_lines_joined)
        self.file_drivers.write("\n]\n")

    def process_item(self, item, spider):
        # Based on item type we store the items
        if isinstance(item, Driver): 
            self.players.append(item)
        else:
            self.teams.append(item)     
        return item """
