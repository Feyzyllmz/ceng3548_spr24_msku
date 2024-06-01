
import scrapy

from formula1.items import Driver, ResultDriver, ResultDriverPersonalInfo, ResultTeam, ResultTeamDetailedInfo, Team

import matplotlib.pyplot as plt
from tkinter import Tk, Button


class QuotesSpider(scrapy.Spider):
    name = "drivers"
    baseUrlForDriversPage = "https://www.formula1.com/en/drivers"
    baseUrlForTeamsPage = "https://www.formula1.com/en/teams.html"
    baseUrlForResultPage = "https://www.formula1.com/en/results.html/2024/races.html"


    def start_requests(self):
        # Call just one request to see result clearly because there are so many data.
        # yield scrapy.Request(url=self.baseUrlForDriversPage, callback=self.parse_direvers_fullnames) # workingg
        yield scrapy.Request(url=self.baseUrlForTeamsPage, callback=self.parse_team_names) # workingg
        yield scrapy.Request(url= self.baseUrlForResultPage, callback=self.parse_result_page_years)        

    # workingg        
    def parse_direvers_fullnames(self, response):
        surnames = response.css(".f1-heading.tracking-normal.text-fs-18px.leading-tight.uppercase.font-bold.non-italic.f1-heading__body.font-formulaOne::text").getall()
        names = response.css(".f1-heading.tracking-normal.text-fs-12px.leading-tight.uppercase.font-normal.non-italic.f1-heading__body.font-formulaOne::text").getall()
        for name,surname in zip(names, surnames):
            driver_full_name = "https://www.formula1.com/en/drivers/" +name.lower() + "-" + surname.lower()
            yield response.follow(driver_full_name, callback=self.parse_driver_page)

    # workingg
    def parse_team_names(self, response):
        teams = response.css(".f1-heading.tracking-normal.text-fs-20px.tablet\:text-fs-25px.leading-tight.normal-case.font-bold.non-italic.f1-heading__body.font-formulaOne::text").getall()
        for team in teams:
            team_name = team.replace(' ', '-')
            team_url = "https://www.formula1.com/en/teams/" + team_name + ".html"
            yield scrapy.Request(team_url, callback=self.parse_team_page)

    # workingg
    def parse_driver_page(self, response):
        driver = Driver()
        all_information=  response.css(".f1-text.font-titillium.tracking-normal.font-normal.non-italic.normal-case.leading-snug.f1-text__body.text-fs-17px.max-laptop\:mb-normal::text").getall()
        fullname = str(response.css(".f1-heading.tracking-normal.text-fs-24px.tablet\:text-fs-42px.leading-tight.normal-case.font-bold.non-italic.f1-heading__body.font-formulaOne::text").get())
        fullname = fullname.split(' ')
        lastname = fullname[len(fullname)-1]
        fullname.pop(len(fullname)-1)
        firstname = ""
        for name in fullname : firstname = firstname + " " + name
        driver.first_name = firstname.strip()
        driver.last_name = lastname
        driver.team =  all_information[0]
        driver.country =  all_information[1]
        driver.podiums =  all_information[2]
        driver.points =  all_information[3]
        driver.grand_prix_entered =  all_information[4]
        driver.world_championships =  all_information[5]
        driver.highest_race_finish = all_information[6]
        driver.highest_grid_position =  all_information[7]
        driver.date_of_birth =  all_information[8]
        driver.place_of_birth = all_information[9]
        yield driver

    # workingg
    def parse_team_page(self, response):
        all_information = response.css(".f1-text.font-titillium.tracking-normal.font-normal.non-italic.normal-case.leading-snug.f1-text__body.text-fs-17px.max-laptop\:mb-normal::text").getall()
        team_drivers_names = response.css(".f1-heading.tracking-normal.text-fs-18px.leading-tight.normal-case.font-normal.non-italic.f1-heading__body.font-formulaOne.mt-xs::text").getall()
        team = Team()
        team.full_team_name = all_information[0]
        team.drivers = team_drivers_names
        team.base = all_information[1]
        team.team_chief = all_information[2]
        team.technical_chief = all_information[3]
        team.chassis = all_information[4]
        team.power_unit = all_information[5]
        team.first_team_entry = all_information[6]
        team.world_championships = all_information[7]
        team.highest_race_finish = all_information[8]
        team.pole_positions = all_information[9]
        team.fastest_laps = all_information[10]
        yield team

    async def parse_result_page_years(self, response):
        count_for_current_year = 0
        result_links_accordingTo_years = response.css("li.resultsarchive-filter-item a::attr(href)").getall()
        for result_link in result_links_accordingTo_years :
            races_link = result_link.split('/')
            if ('races.html' in races_link):
                if '2024' in result_link.split('/'): 
                    if (count_for_current_year == 0):
                        count_for_current_year += 1
                        yield response.follow(url = "https://www.formula1.com"+result_link.replace('races', 'team'), callback=self.parse_result_teams_page)
                        yield response.follow(url = "https://www.formula1.com"+result_link.replace('races', 'drivers'), callback=self.parse_result_drivers_page)

    # workingg
    def parse_result_teams_page(self, response):
        year = response.css(".ResultsArchiveTitle::text").get().strip()[0:4]
        poses = response.css("td.dark::text").getall()[::2]
        teams = response.css(".dark.bold.uppercase.ArchiveLink::text").getall()
        ptses = response.css("td.dark.bold::text").getall()
        teams_urls = response.xpath('//a[@class="dark bold uppercase ArchiveLink"]/@href').getall()
        for url in teams_urls:
            if ('2024' in url.split('/')):
                yield response.follow(url = url, callback = self.parse_result_team_page_details)
        for index,value in enumerate(poses):
            resultTeam = ResultTeam()
            resultTeam.year = year
            resultTeam.pos = value.strip()
            resultTeam.team = teams[index] if index < len(teams) else None
            resultTeam.pts = ptses[index]if index < len(ptses) else None
            yield resultTeam
    
    def parse_result_team_page_details(self, response):
        year = response.css(".ResultsArchiveTitle::text").get().strip().split(':')[0].split(' ')[0]
        team = response.css(".ResultsArchiveTitle::text").get().strip().split(':')[1].strip()
        grand_prixes = response.css(".dark.ArchiveLink::text").getall()
        dates_and_ptses = response.css(".dark.bold::text").getall()
        for index, value in enumerate(grand_prixes):
            resultTeamDetailedInfo = ResultTeamDetailedInfo()
            resultTeamDetailedInfo.year = year
            resultTeamDetailedInfo.team = team
            resultTeamDetailedInfo.grand_prix = value
            resultTeamDetailedInfo.date = dates_and_ptses[(index * 2)]
            resultTeamDetailedInfo.pts = dates_and_ptses[(index *2) + 1]
            yield resultTeamDetailedInfo
            
    # workingg (called only for 2024 drivers)
    def parse_result_drivers_page(self, response):
        cars = response.css(".grey.semi-bold.uppercase.ArchiveLink::text").getall()
        cleaned_cars = [element for element in cars if element.strip() != '']
        driver_names = response.css(".hide-for-tablet::text").getall()
        driver_surnames  = response.css(".hide-for-mobile::text").getall()
        poses_nationalities_ptses = response.css(".dark::text").getall()
        cleaned_poses_nationalities_ptses = [element for element in poses_nationalities_ptses if element.strip() != '']
        drivers_urls = response.xpath('//a[@class="dark bold ArchiveLink"]/@href').getall()

        # workingg (driverların tüm yarışlarıyla ilgili bilgiler)
        for driver_url in drivers_urls:
            yield response.follow(url = driver_url, callback = self.parse_result_drivers_personel_info_page)
        # workingg (driverların personal page'i)
        for name, surname in zip(driver_names, driver_surnames):
            yield response.follow(url = "https://www.formula1.com/en/drivers/" + name.lower() + "-" + surname.lower(), callback=self.parse_driver_page)
        # workingg (results pagedeki driver seçeneğindeki bilgiler)
        for index, value in enumerate(driver_surnames):
            resultDriver = ResultDriver()
            resultDriver.pos = cleaned_poses_nationalities_ptses[index *3]
            resultDriver.driver = driver_names[index] + " " + value
            resultDriver.nationality = cleaned_poses_nationalities_ptses[(index *3)+1]
            resultDriver.car = cleaned_cars[index]
            resultDriver.pts = cleaned_poses_nationalities_ptses[(index *3)+2]
            yield resultDriver
    
    # workingg (for 2024 drivers, result page'deki driverların url'i alınarak çağırılıyor.)
    def parse_result_drivers_personel_info_page(self, response):
        driver = response.css(".ResultsArchiveTitle::text").get().strip().split(':')[1].strip()
        all_information = response.css(".dark::text").getall()
        cars = response.css(".grey.semi-bold.uppercase.ArchiveLink::text").getall()
        for index, value in enumerate(cars):
            resultDriverPersonalInfo = ResultDriverPersonalInfo()
            resultDriverPersonalInfo.driver = driver
            resultDriverPersonalInfo.grand_prix = all_information[index * 4]
            resultDriverPersonalInfo.date = all_information[(index * 4)+1]
            resultDriverPersonalInfo.car = value
            resultDriverPersonalInfo.race_position = all_information[(index * 4)+2]
            resultDriverPersonalInfo.pts = all_information[(index * 4)+3]
            yield resultDriverPersonalInfo

    
                
        