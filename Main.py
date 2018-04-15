import datetime

Days = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]
Months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

def dotw(date):

    day, month, year = (int(x) for x in date.split('/'))
    ans = datetime.date(year, month, day)
    return(ans.strftime("%A"))
    # can return ans to be used as wished

# returns datetime object date as a string
def dt2date(dtdate):
    pieces = str(dtdate).split('-')
    return pieces[2] + "/" + pieces[1] + "/" + pieces[0]

def date2dt(date):
    pieces = date.split('/')
    return pieces[2] + "-" + pieces[1] + "-" + pieces[0]

# Removes spaces at the start and end of a string
def remove_blanks(string):

    while string[-1:] == " ":
        string = string[:-1]
    while string[:1] == " ":
        string = string[1:]

    return string

# Function to check if the input is an integer
def isnumber(input):
    try:
        input = int(input)
    except ValueError:
        return False
    else:
        return True

# Checks an input date, returns false if in the wrong format.
def date_checker(input_date):

    input_date = remove_blanks(input_date)

    if len(input_date) != 10:
        return False

    if isnumber(input_date[:2]) and isnumber(input_date[3:5])\
            and isnumber(input_date[6:10]) and input_date[2] + input_date[5] == "//":
        return input_date
    else:
        return False

# Returns False if the input is not done or hh:mm
def input_cleaner(input_time):

    input_time = remove_blanks(input_time)

    # Main checks on input
    if input_time.lower() == "done":
        return True
    elif len(input_time) != 5:
        return False
    elif isnumber(input_time[:2]) == True and isnumber(input_time[-2:]) == True and input_time[2] ==":":
        return input_time
    else:
        return False

# Returns the string of times associated with a date in the log, False if data not in log
def find_entry(date):

    log = open('log.txt', 'r')

    entries = log.readlines()

    for entry in entries:

        if entry[:10] == date:

            working_day = entry[11:]

            log.close()

            return working_day

    log.close()
    return False

# Calculates the time spent working (mins) for a date in the log, returns False if date not in log
def working_time(date):

    day = find_entry(date)

    if day == False:
        return False

    is_start = 0b1

    x = 0

    work_time = 0

    while x < len(day)-1:

        # if statement to switch between start and end times
        if day[x] == " ":
            is_start ^= 0b1

            x += 1

        if is_start == 0b1:

            start_hour = float(day[x:x + 2])

            start_min = float(day[x + 3:x + 5])

        else:
            end_hour = float(day[x:x + 2])

            end_min = float(day[x + 3:x + 5])


            work_time += (end_hour - start_hour)*60 + (end_min - start_min)
        x += 5

    return work_time

# Calculates the time spent on breaks during the working day.
def break_time(date):

    day = find_entry(date)

    if day == False:
        return False

    day = remove_blanks(day)

    start_hour = float(day[:2])
    start_min = float(day[3:5])
    end_hour = float(day[-6:-4])
    end_min = float(day[-3:])

    total_time = (end_hour - start_hour)*60 + (end_min - start_min)

    resting_time = total_time - working_time(date)

    return resting_time

# Calculates the number of breaks taken in a day.
def break_number(date):

    day = find_entry(date)

    if day == False:
        return False

    day = remove_blanks(day)

    if len(day) < 11:
        return False
    elif len(day) > 11:

        breaknumber = len(day[11:])/12

    else:

        break_number = 1

    return breaknumber

def print_time(mins):

    minute = mins % 60

    hour = (mins - minute) / 60

    if hour == 1:

        if minute == 1:
            return "1hr and 1min"
        elif minute == 0:
            return "1hr"
        else:
            return "1hr and " + str(int(minute)) + "mins"
    elif hour == 0:

        if minute == 1:
            return "1min."
        elif minute > 1:
            return str(int(minute)) + "mins"
        else:
            return "no time at all"

    elif minute == 1:
        return str(int(hour)) + "hrs and 1min"
    elif minute == 0:
        return str(int(hour)) + "hrs"
    else:
        return str(int(hour)) + "hrs and " + str(int(minute)) + "mins"

# Prints the time spent on break on a certain day
def print_break(entry_date):
    mins_break = break_time(entry_date)
    break_minute = mins_break % 60
    break_hour = (mins_break - break_minute) / 60

    break_num = break_number(entry_date)

    if mins_break == 0:
        print("You did not stop working at all, wowwza!")
    else:
        if break_hour == 1:
            if break_minute == 1:
                print("You had 1hr and 1min of time off spread over " + str(int(break_num)) + " breaks during the day.")
            elif break_minute == 0:
                print("You had 1hr of time off spread over " + str(int(break_num)) + " breaks during the day.")
            else:
                print("You had 1hr and " + str(int(break_minute)) +
                      "mins of time off spread over " + str(int(break_num)) + " breaks during the day.")
        elif break_hour == 0:
            if break_minute == 1:
                print("You had just one minute off.... was that really worth it?")
            else:
                print("You had " + str(int(break_minute)) + "mins of time off spread over " + str(int(break_num)) + " breaks during the day.")
        else:
            if break_minute == 1:
                print("You had " + str(int(break_hour)) + "hrs and 1min of time off spread over " + str(int(break_num)) + " breaks during the day.")
            elif break_minute == 0:
                print("You had " + str(int(break_hour)) + "hrs of time off spread over " + str(int(break_num)) + " breaks during the day.")
            else:
                print("You had " + str(int(break_hour)) + "hrs and " + str(int(break_minute)) +
                    "mins of time off spread over " + str(int(break_num)) + " breaks during the day.")

# Prints the time spent on break on a certain day
def print_work(entry_date):

    print('You worked for ' + str(print_time(working_time(entry_date)))+'.')

def week_remaining(date):

    day, month, year = (int(x) for x in date.split('/'))
    dtdate = datetime.date(year, month, day)

    days = {"Monday" : 1,
                        "Tuesday" : 2,
                        "Wednesday" : 3,
                        "Thursday" : 4,
                        "Friday" : 5,
                        "Saturday" : 6,
                        "Sunday" : 7
                       }

    day_number = days[dotw(date)]
    remaining_days = 7 - day_number
    print("Day number - " + str(day_number))
    mins_this_week = 0;
    days_this_week = 0;

    while day_number > 0:

        add_date = dtdate - datetime.timedelta(days = day_number - 1 )

        pull = dt2date(add_date)

        if find_entry(pull) != False:

            mins_this_week += working_time(pull)
            days_this_week += 1

        day_number -= 1

    print("So far this week you have worked on " + str(int(days_this_week)) +
          " days, with a total work time of " + str(print_time(mins_this_week)))

    work_time_target = 35*60

    work_left = work_time_target - mins_this_week

    if work_left < 1:
        print("Congrats, you have met your target work time this week of "
              + print_time(work_time_target) + ".")
    elif remaining_days > 3:
        print("In the remaining " + str(remaining_days - 2) +
              " weekdays you need to average at least " + print_time(work_left//(remaining_days-2)) + " work per day.")
    elif remaining_days == 3:
        print("You only have one day of work left in the standard work week." +
              " Make it count and meet the weekly work target by working " + print_time(work_left) + ".")
    else:
        print("Bad luck, you are out of standard work days. You need to work an extra " + print_time(work_left) + ".")
        print("I guess you could do it this weekend or next week.")

# Function to enter a new entry into the log
def enter_day():

    log = open('log.txt', 'a')

    clean_input = False

    while clean_input == False:

        entry_date = input("Please enter the date for the entry in the format dd/mm/yyyy:")

        entry_date = date_checker(entry_date)

        if entry_date:
            clean_input = True

    log.write(entry_date)

    entry_date = entry_date

    print("Now enter the start and end times of working sessions on this day.")
    print("Use the 24 hr time format, HH:MM, press enter between entries and type done when finished.")

    enter_hours = True

    inputs = []

    while enter_hours:

        clean_input = False
        while clean_input == False:

            new_input = input()
            clean_input = input_cleaner(new_input)

            if clean_input == False:
                print("Please enter a time in the format HH:MM or done when finished.")

        if clean_input == True:
            enter_hours = False
        else:
            inputs.append(clean_input)

    to_write = ""

    for entry in inputs[:-1]:

        to_write = to_write + " " + entry

    to_write = to_write + " " + inputs[-1] + "\n"

    log.write(to_write)

    log.close()

    mins_work = working_time(entry_date)
    mins_break = break_time(entry_date)

    print("You worked " + print_time(working_time(entry_date)))

    print_break(entry_date)

    work_percent = 100 * mins_work / (mins_work + mins_break)
    work_percent = int(work_percent - (work_percent % 1))

    print("You worked for " + str(work_percent) + "% of the working day.")

    week_remaining(entry_date)

# Function to recall a day from the log
def recall_date():

    clean_input = False

    while clean_input == False:

        entry_date = input("Please enter the day you want summarised in the format dd/mm/yyyy:")

        entry_date = date_checker(entry_date)

        if entry_date:
            clean_input = True

    if find_entry(entry_date) == False:

        print("Sorry that data is not in the log")

    else:

        print_work(entry_date)
        print_break(entry_date)

# Function to summarise all log entries... not working
def summarise_log(*args):

    if len(args) == 0:

        startdate = "1990-01-01"
        enddate = "3000-01-01"

    else:

        startdate = date2dt(args[0])
        enddate = date2dt(args[1])

    log = open('log.txt', 'r')

    rawentries = log.readlines()

    entries = []

    for entry in rawentries:

        if date2dt(entry[0:10]) >= startdate and date2dt(entry[0:10]) <= enddate:

            entries.append(entry)

    number_of_entries = len(entries)
    total_work_time = 0
    total_break_time = 0
    most_work = ["",0]
    most_break = ["",0]
    most_breaks = ["",0]
    most_efficiency = ["",0]

    for entry in entries:

        total_work_time += working_time(entry[:10])
        total_break_time += break_time(entry[:10])
        work_percent = 100 * working_time(entry[:10]) / (working_time(entry[:10]) + break_time(entry[:10]))

        if working_time(entry[:10]) > most_work[1]:

            most_work[0] = entry[:10]
            most_work[1] = working_time(entry[:10])

        elif working_time(entry[:10]) == most_work[1]:

            most_work[0] += " and " + entry[:10]

        if break_time(entry[:10]) > most_break[1]:

            most_break[0] = entry[:10]
            most_break[1] = break_time(entry[:10])

        elif break_time(entry[:10]) == most_break[1]:

            most_break[0] += " and " + entry[:10]

        if break_number(entry[:10]) > most_breaks[1]:

            most_breaks[0] = entry[:10]
            most_breaks[1] = break_number(entry[:10])

        elif break_number(entry[:10]) == most_breaks[1]:

            most_breaks[0] += " and " + entry[:10]

        if work_percent > most_efficiency[1]:

            most_efficiency[0] = entry[:10]
            most_efficiency[1] = work_percent

        elif work_percent == most_efficiency[1]:

            most_efficiency[0] += " and " + entry[:10]

    total_work_percent = (100 * total_work_time / (total_work_time + total_break_time)) // 1

    average_work_time = (total_work_time / number_of_entries) // 1
    average_break_time = (total_break_time / number_of_entries) // 1

    print("You have logged {0} days work, averaging {1} work per day.".format(str(number_of_entries), print_time(average_work_time)))
    print("You worked the longest on {0}, working {1} .".format(str(most_work[0]), print_time(most_work[1])))


def mainselector():
    print("Welcome to the work logger, you have the following options:")

    selection = True
    while selection:

        print("Press 1 to enter a new day into the log.")
        print("Press 2 to view the log for a day.")
        print("Press 3 to view a work log summary.")
        print("Press 4 to quit.")

        choice = input()

        if choice == "1":

            enter_day()

            choice = input("If you want to quit, enter 1, otherwise, enter 0.")

            if choice != "0":
                selection = False

        elif choice == "2":

            recall_date()

            choice = input("If you want to quit, enter 1, otherwise, enter 0.")

            if choice != "0":

                selection = False

        elif choice == "3":
            summarise_log()

            choice = input("If you want to quit, enter 1, otherwise, enter 0.")

            if choice != "0":

                selection = False

        elif choice == "4":
            print("Quitting")
            selection = False

    print("Thank you for using the work logger.")


if __name__ == "__main__":
    mainselector()

