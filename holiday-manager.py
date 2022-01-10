from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import calendar

@dataclass
class Holiday:
    name: str
    date: datetime     
    
    def __str__ (self):
        return self.name + " (" + str(self.date) + ")"

@dataclass
class HolidayList:
    innerHolidays: list
   
    def addHoliday(self):

        add_holiday = True
        while add_holiday:
            print("Add a Holiday \n==============")
            input_name = input("Holiday: ")
            
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
                        print("Invalid date format!")
                        continue

                if input_holiday not in self.innerHolidays:
                    self.innerHolidays.append(input_holiday)
                    print("Success! " + str(input_holiday) + " has been added to the Holiday Manager.\n")
                    add_holiday = False
                    break

                else:
                    print("\nThat holiday name and date combination is already in the system, try another holiday or leave name blank to return to main menu.\n")

    #def findHoliday(self):
        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(self):
        
        print("Remove a Holiday\n===================")
        
        holiday_input = True
        while holiday_input:
            input_name = input("Holiday: ")
            input_date = input("Date (format: Jan 10, 2022): ")
            input_date = (datetime.strptime(input_date, "%b %d, %Y")).date()

            holiday = Holiday(input_name, input_date)

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
                
                for holiday in self.innerHolidays:
                    save_list.append(holiday.__dict__)

                save_dict = {"holidays": save_list}
                json.dump(save_dict,file,indent = 4,default = str)
        
    def scrapeHolidays(self):

        years = [2020, 2021, 2022, 2023, 2024]
        for year in years:
            
            response = requests.get(f"https://www.timeanddate.com/holidays/us/{year}")
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            entries = soup.find_all('tr')

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
    
    #def filter_holidays_by_week(self, year, week_number):

        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    # def displayHolidaysInWeek(holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    # def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    # def viewCurrentWeek():
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results



def main():

    holiday_list = HolidayList([])
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

        #elif menu_choice == '4':
        
        elif menu_choice == '5':
            print("Exit\n=====")
            exit_input = input("Are you sure you want to exit? Any unsaved changes will be lost [y/n]: ")

            if exit_input == "y":
                print("Goodbye!")
                main_menu = False
            
            else:
                print("Okay, taking you back to main menu.")
        
        else:
            print("That is not a valid option, please try a number 1-5.")


        
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

if __name__ == "__main__":
    main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.