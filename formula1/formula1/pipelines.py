import json

from itemadapter import ItemAdapter

from formula1.items import Driver, ResultDriver, ResultDriverPersonalInfo, ResultTeam, ResultTeamDetailedInfo



class Formula1Pipeline:
    def open_spider(self, spider):
        self.file_drivers = open("drivers.json", "w")
        self.file_drivers.write("[\n")  
        self.drivers = []

        self.file_teams = open("teams.json", "w")
        self.file_teams.write("[\n")  
        self.teams = []

        self.file_result_drivers = open("result_drivers.json", "w")
        self.file_result_drivers.write("[\n")  
        self.resultDrivers = []

        self.file_result_drivers_personal_infos = open("result_drivers_personal_infos.json", "w")
        self.file_result_drivers_personal_infos.write("[\n")  
        self.resultDriversPersonalInfos = []


        self.file_result_teams = open("result_teams.json", "w")
        self.file_result_teams.write("[\n")  
        self.resultTeams = []

        self.file_result_teams_detailed_infos = open("result_teams_detailed_info.json", "w")
        self.file_result_teams_detailed_infos.write("[\n")  
        self.resultTeamsDetailedInfos = []


    def close_spider(self, spider):
        driver_lines = [
            "\t" + json.dumps(ItemAdapter(p).asdict())
            for p in self.drivers
        ]
        drivers_lines_joined = ",\n".join(driver_lines)
        self.file_drivers.write(drivers_lines_joined)
        self.file_drivers.write("\n]\n")

        team_lines = [
            "\t" + json.dumps(ItemAdapter(p).asdict())
            for p in self.teams
        ]
        team_lines_joined = ",\n".join(team_lines)
        self.file_teams.write(team_lines_joined)
        self.file_teams.write("\n]\n")

        result_driver_lines = [
            "\t" + json.dumps(ItemAdapter(p).asdict())
            for p in self.resultDrivers
        ]
        result_driver_lines_joined = ",\n".join(result_driver_lines)
        self.file_result_drivers.write(result_driver_lines_joined)
        self.file_result_drivers.write("\n]\n")

        result_drivers_personal_infos_lines = [
            "\t" + json.dumps(ItemAdapter(p).asdict())
            for p in self.resultDriversPersonalInfos
        ]
        result_drivers_personal_infos_lines_joined = ",\n".join(result_drivers_personal_infos_lines)
        self.file_result_drivers_personal_infos.write(result_drivers_personal_infos_lines_joined)
        self.file_result_drivers_personal_infos.write("\n]\n")

        result_team_lines = [
            "\t" + json.dumps(ItemAdapter(p).asdict())
            for p in self.resultTeams
        ]
        result_team_lines_joined = ",\n".join(result_team_lines)
        self.file_result_teams.write(result_team_lines_joined)
        self.file_result_teams.write("\n]\n")

        result_teams_detailed_infos_lines = [
            "\t" + json.dumps(ItemAdapter(p).asdict())
            for p in self.resultTeamsDetailedInfos
        ]
        result_teams_detailed_infos_lines_joined = ",\n".join(result_teams_detailed_infos_lines)
        self.file_result_teams_detailed_infos.write(result_teams_detailed_infos_lines_joined)
        self.file_result_teams_detailed_infos.write("\n]\n")

    def process_item(self, item, spider):
        # Based on item type we store the items
        if isinstance(item, Driver): 
            self.drivers.append(item)
        elif isinstance(item, ResultDriver):
            self.resultDrivers.append(item)
        elif isinstance(item, ResultDriverPersonalInfo):
            self.resultDriversPersonalInfos.append(item)
        elif isinstance(item, ResultTeam):
            self.resultTeams.append(item)
        elif isinstance(item, ResultTeamDetailedInfo):
            self.resultTeamsDetailedInfos.append(item)
        else:
            self.teams.append(item)     
        return item
