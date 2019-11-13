import re
from datetime import datetime

from final_database import stalls


############################################################################################
################################### displaying of stalls ###################################
############################################################################################


#display stalls which have special menu on certain days. eg. christmas, new years day
def display_special_stall(date):
    date_array = re.split('[-| |:]', date)  # splits date into array of elements
    today = datetime(int(date_array[2]), int(date_array[1]), int(date_array[0]), int(date_array[3]), int(date_array[4]), 0, 0)
    print(today.strftime('%A') + ', ' + today.strftime('%d %B %Y') + ', ' + today.strftime('%H%M') + 'h\n')
    time = date_array[3] + date_array[4]
    dict_of_stalls = print_stall(time)                                                                                  #returns a dictionary of stalls which are open
    print('\n[0] Exit\n')
    while True:                                                                                                         #while loop to keep prompting user until correct input is receieved
        try:
            user_input = int(input(''))
            if user_input in dict_of_stalls:                                                                            #user will key in a number, eg. 1, and if it matches the key in dict_of_stalls, enter the if clause
                stall_sel = dict_of_stalls[user_input]                                                                  #loads the stall name to stall_sel based on user selection
                print(today.strftime('%A') + ', ' + today.strftime('%d %B %Y') + ', ' + today.strftime('%H%M') + 'h')
                print(stall_sel + ' stall\n')
                print('Today\'s special: ')
                display_sel_stall_special_menu(stall_sel, 'special')                                                    #displays special menu of selected stall. eg. 'Chinese' 'special'
                print('')
                display_sel_stall_all_menu(stall_sel, check_type_of_meal(time))                                             #displays all the menu item for the current meal type. eg. 'Chinese' 'breakfast'
                break
            elif user_input == 0:                                                                                       #exits to main menu
                main()
                break
            else:
                print('Wrong input')
        except ValueError:                                                                                              #error handling for when user inputs bad value
            print('Wrong input')


#displays all the stalls. if stalls are not open, it will not be selectable and will show their opening timing
def display_all_stalls(date):                                                                                                 #creates empty array to store all closed stalls at the given current time
    date_array = re.split('[-| |:]', date)                                                                              #splits date into array of elements
    today = datetime(int(date_array[2]), int(date_array[1]), int(date_array[0]), int(date_array[3]), int(date_array[4]), 0, 0)
    weekday = today.weekday() + 1                                                                                       #gets the weekday number. mon = 1, tues = 2. correct way should be datetime.today().weekday() to be able to use the weekday() function. the today() argument holds many required values (year, month, day, hour, min, sec, milisec) which is why I had to split the input date
    print(today.strftime('%A') + ', ' + today.strftime('%d %B %Y') + ', ' + today.strftime('%H%M') + 'h\n')
    time = date_array[3] + date_array[4]                                                                                #gets the time in the format 0000
    dict_of_stalls = print_stall(time)                                                                                  # returns a dictionary of stalls which are open
    print('\n[0] Exit\n')
    odd_or_even_menu(dict_of_stalls, weekday, today, time)


#display stall by user input date
def display_stall_by_date():
    date = date_time_check()                             #gets date which user entered
    day = date.split('-')[0]                        #splits date string seperated by - into an array. stores first element in array to day
    month = date.split('-')[1]                      #splits date string seperated by - into an array. stores second element in array to day
    if int(day) == 25 and int(month) == 12:         #compares if date entered is a special day. 25/12 is christmas
        display_special_stall(date)
    elif int(day) == 1 and int(month) == 1:         #compares if date entered is a special day. 01/01 is new years day
        display_special_stall(date)
    else:                                           #if not special day, display normal menu
        display_all_stalls(date)


def print_stall(time):
    dict_of_stalls = {}                                         # creates an empty dictionary to compare user input with stall
    index = 0
    open_stalls = []                                                                # creates empty array to store all open stalls at the given current time
    closed_stalls = []                                                              # creates empty array to store all closed stalls at the given current time
    for stall_name, stall_details in stalls.items():                                                                    #gets the key to item pair from database. eg. Chinese: { dict of stuff }
        for details_key, details in stall_details.items():                                                              #gets the key to item pair from { dict of stuff }. eg. Breakfast: { dict of breakfast dishes }
            if details_key == 'information':                                                                            #if the key = information, to get the opening hours
                open_time = details['open_hour'][:4]                                                                    #splice the string of opening hours. eg. 0800h - 2000h = 0800
                close_time = details['open_hour'][7:12]                                                                 #splice the string of opening hours. eg. 0800h - 2000h = 2000
                if check_if_stall_open(open_time, close_time,time):                                                     #check if stall is open based on database opening hours
                    index += 1
                    dict_of_stalls[index] = stall_name                                                                  #insert a number to stall name if it is open. eg. 1: 'Chinese'
                    open_stalls.append('[' + '{:<1}'.format(index) + '] ' + '{:<10}'.format(stall_name))                #append to open stalls array if open
                else:
                    closed_stalls.append(stall_name + ' stall is not open. Opening hours: ' + details['open_hour'])     #append to closed stalls array if closed
    for stall in open_stalls:                                                                                           #loop through all of element in open stalls array
        print(stall)
    print('')
    for stall in closed_stalls:                                                                                         #loop through all of element in closed stalls array
        print(stall)
    return dict_of_stalls


##############################################################################
################################### checks ###################################
##############################################################################


#checks the type of meal from the time. returns breakfast or lunch or dinner
def check_type_of_meal(time):
    if 600 <= int(time) < 1200:             #if current time is between 800 - 1159, return breakfast menu
        return 'breakfast'
    elif 1200 <= int(time) < 1800:          #if current time is between 1200 - 1759, return lunch menu
        return 'lunch'
    elif 1800 <= int(time) <= 2200:         #if current time is between 1800 - 2200, return dinner menu
        return 'dinner'


#checks if stall is open by comparing the opening and closing time. returns true or false
def check_if_stall_open(open_time, close_time, time):
    if int(open_time) <= int(time) < int(close_time):       #compares current time to stall opening and closing time
        return True                                         #returns True if within open and close time
    else:
        return False                                        #returns False if not within open and close time


#returns the day of week number. monday = 1, tuesday = 2, etc
def check_day_of_week():
    return datetime.today().weekday() + 1


#check if date input is correct format and a valid date
def date_time_check():
    now = datetime.now()  # gets current date and time when program run
    while True:                                                                     #while loop to keep prompting user until correct input is receieved
        try:
            input_date = input('Enter date in dd-mm-yyyy: ')                        #request for date
            date_array = input_date.split('-')                                      #splits input date into array
            input_date_to_compare = date_array[2] + date_array[1] + date_array[0]   #arrange the input date as yyyymmdd in order to compare
            current_date_to_compare = now.strftime('%Y-%m-%d').replace('-', '')     #arrange current time in the order yyyymmdd in order to compare
            one_year_from_now = int(now.strftime('%Y')) + 1
            one_year_later = str(one_year_from_now) + now.strftime('%m-%d').replace('-', '')
            if datetime.strptime(input_date, '%d-%m-%Y'):                           #if the input date is a valid format of dd-mm-yyyy
                if current_date_to_compare <= input_date_to_compare <= one_year_later:                #input date is either today or some other day in the future
                    pass
                    break
                else:
                    print('Sorry, enter a future date within 1 year from now.\n')
            else:
                print('Wrong date format\n')
        except (ValueError, IndexError):                                                          #error handling
            print('Wrong date format \n')
    while True:
        try:
            input_time = input('Enter time in 0000: ')
            if 0000 <= int(input_time) <= 2359 and len(input_time) == 4:
                input_time = input_time[:2] + ':' + input_time[2:]
                input_date_time = input_date + ' ' + input_time
                return input_date_time
            else:
                print('Wrong time format.\n')
        except ValueError:
            print('Wrong time format.\n')


#calculate queue time
def queue_time(mins):
    people = no_of_people()
    return int(people) * int(mins)


#funtion to return valid number of people the user entered
def no_of_people():
    while True:
        try:
            people = int(input('Enter number of people in queue: '))
            if people > 0:
                return people
            else:
                print('Please input 1 or more.\n')
        except ValueError:
            print('Wrong input\n')


###################################################################################################
################################### display selected stall menu ###################################
###################################################################################################


#displays special menu of selected stall
def display_sel_stall_special_menu(name_of_stall, type_of_meal):
    stall = stalls[name_of_stall]                                           #assigns stall name to stall
    for stall_key, details in stall.items():                                #gets the key to item pair in stall dictionary. eg. chinese: { details }
        if stall_key == type_of_meal:                                       #compares stall key (breakfast, lunch, etc) to the type of meal (breakfast, lunch, etc)
            for details_key, item in details.items():                       #gets the key value pair of stall details. eg. breakfast: { breakfast items }
                print('{:<30}'.format(item['name']), item['price'])


#choose to display the odd or even menu
def odd_or_even_menu(dict_of_stalls, weekday, today, time):
    while True:                                                                                                         #while loop to keep prompting user until correct input is receieved
        try:
            user_input = int(input(''))
            if user_input in dict_of_stalls:                                                                            #user will key in a number, eg. 1, and if it matches the key in dict_of_stalls, enter the if clause
                stall_sel = dict_of_stalls[user_input]                                                                  #loads the stall name to stall_sel based on user selection
                if weekday % 2 == 0:                                                                                    #used to determine what type of menu to show, odd or even depending on weekday
                    print(today.strftime('%A') + ', ' + today.strftime('%d %B %Y') + ', ' + today.strftime('%H%M') + 'h')
                    print(stall_sel + ' stall\n')
                    display_sel_stall_even_menu(stall_sel, check_type_of_meal(time))                                        #display even menu for even days. eg, 2,4,6
                    break
                else:
                    print(today.strftime('%A') + ', ' + today.strftime('%d %B %Y') + ', ' + today.strftime('%H%M') + 'h')
                    print(stall_sel + ' stall\n')
                    display_sel_stall_odd_menu(stall_sel, check_type_of_meal(time))                                         #display odd menu for odd days. eg, 1,3,5,7
                    break
            elif user_input == 0:                                                                                       #exits to main menu
                main()
                break
            else:
                print('Wrong input')
        except ValueError:                                                                                              #error handling for when user inputs bad value
            print('Wrong input')


#displays the user selected stall menu
def display_sel_stall_all_menu(name_of_stall, type_of_meal):
    stall = stalls[name_of_stall]                                       #assigns stall name to stall
    for stall_key, details in stall.items():                            #gets the key to item pair in stall dictionary. eg. chinese: { details }
        if stall_key == type_of_meal:                                   #compares stall key (breakfast, lunch, etc) to the type of meal (breakfast, lunch, etc)
            for details_key, item in details.items():                   #gets the key value pair of stall details. eg. breakfast: { breakfast items }
                print('{:<30}'.format(item['name']), item['price'])
    print('\n[1] Calculate queue time')
    print('\n[0] Exit\n')
    stall_menu_loop(name_of_stall)


#displays the user selected stall menu that have odd number as key
def display_sel_stall_odd_menu(name_of_stall, type_of_meal):
    stall = stalls[name_of_stall]                                           #assigns stall name to stall
    for stall_key, details in stall.items():                                #gets the key to item pair in stall dictionary. eg. chinese: { details }
        if stall_key == type_of_meal:                                       #compares stall key (breakfast, lunch, etc) to the type of meal (breakfast, lunch, etc)
            for details_key, item in details.items():                       #gets the key value pair of stall details. eg. breakfast: { breakfast items }
                if int(details_key) % 2 == 1:                               #prints menu item only if the key is odd
                    print('{:<30}'.format(item['name']), item['price'])
    print('\n[1] Calculate queue time')
    print('\n[0] Exit\n')
    stall_menu_loop(name_of_stall)


#display the user selected stall menu that have even number as key
def display_sel_stall_even_menu(name_of_stall, type_of_meal):
    stall = stalls[name_of_stall]                                           #assigns stall name to stall
    for stall_key, details in stall.items():                                #gets the key to item pair in stall dictionary. eg. chinese: { details }
        if stall_key == type_of_meal:                                       #compares stall key (breakfast, lunch, etc) to the type of meal (breakfast, lunch, etc)
            for details_key, item in details.items():                       #gets the key value pair of stall details. eg. breakfast: { breakfast items }
                if int(details_key) % 2 == 0:                               #prints menu item only if the key is even
                    print('{:<30}'.format(item['name']), item['price'])
    print('\n[1] Calculate queue time')
    print('\n[0] Exit\n')
    stall_menu_loop(name_of_stall)


#################################################################################################
################################### loops to check user input ###################################
#################################################################################################


#get user input to either exit to main menu or calculate queue time when user is at stall menu screen
def stall_menu_loop(name_of_stall):
    while True:                                                             #while loop to keep prompting user until correct input is receieved
        try:
            user_input = int(input(''))
            if user_input == 0:                                             #exits to main menu
                menu()
                break
            elif user_input == 1:
                stall_queue_time = stalls[name_of_stall]['queue_time']
                total_queue_time = queue_time(stall_queue_time)
                print('You will have to wait approximately', total_queue_time, 'minutes for', name_of_stall, 'stall')
                print('\n[0] Exit\n')
                exit_loop()
                break
            else:
                print('Wrong input\n')
        except ValueError:                                                  #error handling
            print('Wrong input\n')


#exits to main() if user input is 0
def exit_loop():
    while True:
        try:
            exit_input = int(input(''))
            if exit_input == 0:
                main()
                break
            else:
                print('Wrong input\n')
        except ValueError:
            print('Wrong input\n')


############################################################################
################################### menu ###################################
############################################################################


#menu where user will select what they want to view or do
def menu():
    now = datetime.now()  # gets current date and time when program run
    date_time_string = now.strftime('%d-%m-%Y %H:%M')  # stores current date in dd-mm-yyyy format to date_string
    while True:                                                     #while loop to keep prompting user until correct input is receieved
        try:
            print('[1] View all stalls')
            print('[2] View stalls by date')
            print('\n[0] Exit\n')
            user_input = int(input(''))
            if user_input == 1:
                display_all_stalls(date_time_string)        #view all stalls with the current date as argument
                break
            elif user_input == 2:
                display_stall_by_date()                             #runs the display stall by date function
                break
            elif user_input == 0:                                   #exits the loop
                exit()
            else:
                print('Wrong input\n')
        except ValueError:
            print('Wrong input\n')


#main menu
def main():
    print('\n')
    print('Welcome to the virtual coffee shop!')
    print('Please select your choice..')
    print('\n')
    menu()


main()
