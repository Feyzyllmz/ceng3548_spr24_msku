import json
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "drivers"

    def start_requests(self):
        baseUrlForDriversPage = "https://www.formula1.com/en/drivers"
        baseUrlForTeamsPage = "https://www.formula1.com/en/teams.html"
        baseUrlForResultPage = "https://www.formula1.com/en/results.html/2024/races.html"
        # Call just one request to see result clearly because there are so many data.
        yield scrapy.Request(url=baseUrlForDriversPage, callback=self.parse_direvers_fullnames)
        yield scrapy.Request(url=baseUrlForTeamsPage, callback=self.parse_team_names)
        yield scrapy.Request(url= baseUrlForResultPage, callback=self.parse_result_page_years)
            
    def parse_direvers_fullnames(self, response):
        surnames = response.css(".f1-heading.tracking-normal.text-fs-18px.leading-tight.uppercase.font-bold.non-italic.f1-heading__body.font-formulaOne::text").getall()
        names = response.css(".f1-heading.tracking-normal.text-fs-12px.leading-tight.uppercase.font-normal.non-italic.f1-heading__body.font-formulaOne::text").getall()
        for name,surname in zip(names, surnames):
            driver_full_name = "https://www.formula1.com/en/drivers/" +name.lower() + "-" + surname.lower()
            yield response.follow(driver_full_name, callback=self.parse_driver_page)

    def parse_team_names(self, response):
        teams = response.css(".f1-heading.tracking-normal.text-fs-20px.tablet\:text-fs-25px.leading-tight.normal-case.font-bold.non-italic.f1-heading__body.font-formulaOne::text").getall()
        for team in teams:
            team_name = team.replace(' ', '-')
            team_url = "https://www.formula1.com/en/teams/" + team_name + ".html"
            yield response.follow(team_url, callback=self.parse_team_page)

    def parse_driver_page(self, response):
        all_information=  response.css(".f1-text.font-titillium.tracking-normal.font-normal.non-italic.normal-case.leading-snug.f1-text__body.text-fs-17px.max-laptop\:mb-normal::text").getall()
        fullname = str(response.css(".f1-heading.tracking-normal.text-fs-24px.tablet\:text-fs-42px.leading-tight.normal-case.font-bold.non-italic.f1-heading__body.font-formulaOne::text").get())
        fullname = fullname.split(' ')
        lastname = fullname[len(fullname)-1]
        fullname.pop(len(fullname)-1)
        firstname = ""
        for name in fullname : firstname = firstname + " " + name
        driver_data = {
            "First Name" : firstname,
            "Last Name" : lastname,
            "Team" : all_information[0],
            "Country" : all_information[1],
            "Podiums" : all_information[2],
            "Points" : all_information[3],
            "Grands Prix entered" : all_information[4],
            "World Championships" : all_information[5],
            "Highest race finish" : all_information[6],
            "Highest grid position" : all_information[7],
            "Date of birth" : all_information[8],
            "Place of birth" : all_information[9]
        }
        yield driver_data

    def parse_team_page(self, response):
        all_information = response.css(".f1-text.font-titillium.tracking-normal.font-normal.non-italic.normal-case.leading-snug.f1-text__body.text-fs-17px.max-laptop\:mb-normal::text").getall()
        team_drivers_names = response.css(".f1-heading.tracking-normal.text-fs-18px.leading-tight.normal-case.font-normal.non-italic.f1-heading__body.font-formulaOne.mt-xs::text").getall()
        team_data = {
            "Full Team Name" : all_information[0],
            "Drivers" : team_drivers_names,
            "Base" : all_information[1],
            "Team Chief" : all_information[2],
            "Technical Chief" : all_information[3],
            "Chassis" : all_information[4],
            "Power Unit" : all_information[5],
            "First Team Entry" : all_information[6],
            "World Championships" : all_information[7],
            "Highest Race Finish" : all_information[8],
            "Pole Positions" : all_information[9],
            "Fastest Laps" : all_information[10]
        }
        return team_data

    def parse_result_page_years(self, response):
        print(response.url)
        result_links_accordingTo_years = response.css("li.resultsarchive-filter-item a::attr(href)").getall()
        for result_link in result_links_accordingTo_years :
            # Below commended line is still in progress. Not working properly.
            # yield response.follow(url = "https://www.formula1.com"+result_link, callback = self.parse_result_races_page)
            yield response.follow(url = "https://www.formula1.com"+result_link.replace('races', 'team'), callback=self.parse_result_team_page)
    def parse_result_races_page(self, response) : 
        result_table = []
        grand_prixs = response.css(".dark.bold.ArchiveLink::text").getall()
        grand_prix_urls = response.css(".dark.bold.ArchiveLink a::attr(href)").getall()
        dates = response.css(".dark.hide-for-mobile::text").getall()
        winners = response.css(".hide-for-mobile::text").getall()
        cars = response.css(".semi-bold.uppercase::text").getall()
        laps = response.css(".bold.hide-for-mobile::text").getall()
        times = response.css(".dark.bold.hide-for-tablet::text").getall()
        print(grand_prixs[0].strip())
        for index,value in enumerate(grand_prixs):  
            result_data = {
                "GRAND PRIX": grand_prixs[index].strip(),
                "DATE" :dates[index],
                "WINNER" : winners[index],
                "CAR" : cars[index],
                "LAPS" : laps[index],
                "TIME" : times[index]
            }
            result_table.append(result_data)
        
    
    def parse_result_team_page(self, response):
        result_table = []
        year = response.css(".ResultsArchiveTitle::text").get().strip()[0:4]
        poses = response.css("td.dark::text").getall()[::2]
        teams = response.css(".dark.bold.uppercase.ArchiveLink::text").getall()
        ptses = response.css("td.dark.bold::text").getall()
        for index,value in enumerate(poses):
            result_data = {
                "YEAR" : year,
                "POS" : poses[index].strip(),
                "TEAM" : teams[index],
                "PTS" : ptses[index]
            }
            result_table.append(result_data)
        return result_table




                
        