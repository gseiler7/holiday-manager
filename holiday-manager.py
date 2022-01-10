from datetime import date, datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

@dataclass
class Holiday:
    name: str
    date: datetime     
    
    def __str__ (self):
        return self.name + " (" + str(self.date) + ")"

    def __repr__ (self):
        return {self.name: str(self.date)}

    def getDate (self):
        return self.date

@dataclass
class HolidayList:
    innerHolidays: list
   
    def addHoliday(self):

        add_holiday = True
        while add_holiday:
            print("Add a Holiday \n==============")
            input_name = input("Holiday: ")
            
            # way to exit to main menu if holiday is already in holiday manager
            if input_name == '':
                add_holiday = False
                break

            else:
                date_input = True
                while date_input:
                    input_date = input("Date (format: Jan 10, 2022): ")

                    try:
                        input_date = (datetime.strptime(input_date, "%b %d, %Y")).date()
                        input_holiday = Holiday(input_name, input_date)
                        date_input = False
                        break
                    except:
                        print("Error: invalid date format. Format example: Jan 10, 2022")
                        continue
                
                # check if holiday is already in innerHolidays = no duplicates!
                if input_holiday not in self.innerHolidays:
                    self.innerHolidays.append(input_holiday)
                    print("Success! " + str(input_holiday) + " has been added to the Holiday Manager.\n")
                    add_holiday = False
                    break

                else:
                    print("\nError: that holiday name and date combination is already in the system. Try another holiday or leave name blank to return to main menu.\n")

    def removeHoliday(self):
        
        print("Remove a Holiday\n===================")
        
        holiday_input = True
        while holiday_input:
            input_name = input("Holiday: ")
            input_date = input("Date (format: Jan 10, 2022): ")
            input_date = (datetime.strptime(input_date, "%b %d, %Y")).date()

            holiday = Holiday(input_name, input_date)

            # check if holiday is in innerHolidays
            if holiday in self.innerHolidays:
                self.innerHolidays.remove(holiday)
                print("Success: " + input_name + " has been removed from the holiday list.")
                holiday_input = True
                break

            else:
                print("Error: holiday not found in holiday list as input.")

    def read_json(self, filelocation):
        
        with open(filelocation,"r") as file:
            read = json.load(file)

            for holiday in read["holidays"]:
                read_holiday = Holiday(holiday["name"], (datetime.strptime(holiday["date"], "%Y-%m-%d")).date())
                
                if read_holiday not in self.innerHolidays:
                    self.innerHolidays.append(read_holiday)
                
                else:
                    pass

    def save_to_json(self, filename):
            
            save_list = []
            
            with open(filename + ".json", "w") as file:
                
                # put holidays into dictionary
                for holiday in self.innerHolidays:
                    save_list.append(holiday.__dict__)

                # json format as given in original file
                save_dict = {"holidays": save_list}
                json.dump(save_dict,file,indent = 4,default = str)
        
    def scrapeHolidays(self):

        years = [2020, 2021, 2022, 2023, 2024]
        for year in years:
            
            response = requests.get(f"https://www.timeanddate.com/holidays/us/{year}")
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            entries = soup.find_all('tr')

            # find holiday name and date information, put into Holiday object
            for entry in entries:
                try:
                    holiday_name = entry.find('a').string
                    holiday_date = entry.find('th', attrs = {'class':'nw'}).string + ', ' + str(year)
                    holiday_date = (datetime.strptime(holiday_date, "%b %d, %Y")).date()
                    holiday_entry = Holiday(holiday_name, holiday_date)
                    
                    if holiday_entry not in self.innerHolidays:
                        self.innerHolidays.append(holiday_entry)

                    else:
                        pass
                except:
                    pass

    def numHolidays(self):

        return len(self.innerHolidays)

    def filter_holidays_by_week(self, year, week):

            # filter holidays into a list based on the input year, week
            holidays = list(filter(lambda holiday: holiday.getDate().isocalendar()[0] == year and holiday.getDate().isocalendar()[1] == int(week),self.innerHolidays))
            
            for holiday in holidays:
                print(holiday)

    def displayHolidaysInWeek(self):
        
        print("View Holidays\n==============")
        years = [2020, 2021, 2022, 2023, 2024]
        weeks = [num for num in range(1,53)]

        # get input year, week
        week_input = True
        year_input = True
        while year_input:

            if week_input == False:
                break
            
            input_year = int(input("Which year?: "))

            if input_year not in years:
                print("Error: invalid year input. Please select a year within the range 2020-2024.")
            
            else:
                year_input = True
                week_input = True
                while week_input:
                    input_week = input("Which week? #[1-52, leave blank for current week]: ")
                    
                    if input_week == '':
                        week_input = False
                        break

                    if int(input_week) not in weeks:
                        print("Error: invalid week input. Please select a week within the range 1-52, or leave blank.")
                    
                    else:
                        week_input = False
                        break
        
        if input_week == "":
            self.viewCurrentWeek()
        
        elif int(input_week) in weeks:
            self.filter_holidays_by_week(input_year, input_week)

    def getWeather(self, year, week):

        # day range based on year and week number (current year and week)
        week_start = str(date.fromisocalendar(year, week, 1))
        week_end = str(date.fromisocalendar(year, week, 7))
        
        # query API
        url = "https://weatherapi-com.p.rapidapi.com/history.json"

        querystring = {"q":"Minneapolis","dt": week_start,"lang":"en","hour":"12","end_dt": week_end}

        headers = {
                'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
                'x-rapidapi-key': "0aaee5e951mshc8b68c45d295ffep1bd825jsnf91bc5c7f0fe"
        }

        response = requests.get(url, headers=headers, params=querystring)

        data_dict = {}
        
        weather_dict = response.json()

        # print weather information from API
        for day in [1,2,3,4,5,6,7]:
            try:
                data_dict[str(date.fromisocalendar(year, week, day))] = weather_dict["forecast"]["forecastday"][day]["day"]["condition"]["text"]
            except:
                data_dict[str(date.fromisocalendar(year, week, day))] = "Weather data not available"

        print("Weather:")
        print(data_dict)

    def viewCurrentWeek(self):

        # find current year and week from date
        current_date = date.today().isocalendar()
        current_year = current_date[0]
        current_week = current_date[1]
        
        # prompt for weather, show holidays and weather or just holidays
        weather_input = True
        while weather_input:

            input_weather = input("Would you like to see this week's weather? [y/n]: ")
                
            if input_weather == 'y':
                self.filter_holidays_by_week(current_year, current_week)
                self.getWeather(current_year, current_week)
                weather_input = False
                break
                
            elif input_weather == 'n':
                self.filter_holidays_by_week(current_year, current_week)
                weather_input = False
                break



def main():
    
    # initialize HolidayList object
    holiday_list = HolidayList([])

    # add holidays to list from file and scraping timeanddate.com
    holiday_list.scrapeHolidays()
    holiday_list.read_json("holidays.json")

    main_menu = True
    while main_menu:

        print("\nHoliday Management \n==================")
        holiday_count = str(holiday_list.numHolidays())
        print("There are " + holiday_count + " holidays stored in the system.\n")
        print("Holiday Menu \n==============")
        print("1. Add a Holiday \n2. Remove a Holiday \n3. Save Holiday List \n4. View Holidays \n5. Exit\n")
        
        menu_choice = input("Please input the number of the menu action you would like to take: ")

        if menu_choice == '1':
            holiday_list.addHoliday()

        elif menu_choice == '2':
            holiday_list.removeHoliday()

        elif menu_choice == '3':
            print("Saving Holiday List \n=================")
            save_input = input("Are you sure you want to save your changes? [y/n]: ")

            if save_input == 'y':
                filename = input("Filename: ")
                holiday_list.save_to_json(filename)

            elif save_input == 'n':
                print("Save canceled.\n")

        elif menu_choice == '4':
            holiday_list.displayHolidaysInWeek()
        
        elif menu_choice == '5':
            print("Exit\n=====")
            exit_input = input("Are you sure you want to exit? Any unsaved changes will be lost [y/n]: ")

            if exit_input == "y":
                print("Goodbye!")
                main_menu = False
            
            else:
                print("Okay, taking you back to main menu.")
        
        else:
            print("Error: invalid input. Please try a number 1-5.")

if __name__ == "__main__":
    main()