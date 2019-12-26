import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ["January", "February", "March", "April", "May", "June"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
filter_options = [1, 2, 3]
raw_data_ans = ["yes", "no"]

""" 
General comments just for the sake of the Git commands project.
I am adding comments
"""

def generate_dataframe_in_chunks(df, nrows):
    """Yield successive chunks from a dataframe of number of rows equal to nrows."""
    row = 0
    while row <= df.shape[0]:
        yield df[row:row + nrows]
        row += nrows

def print_my_name(name):
    print(name)

def has_guessed_my_wife_name():
    name = str(input("Do you want to see raw data? yes or no\n"))
    return name.capitalize == "Noela"

def display_raw_data(dataframe, nrows):
    """
    This functions asks the user if he or she wants to see the raw data.
    If he answer yes, raw data are displayed nrows rows at a time.
    """
    dataframe_gen = generate_dataframe_in_chunks(dataframe, nrows)
    while True:
        try:
            wants_to_see_raw_data = input("Do you want to see raw data? yes or no\n")
            assert wants_to_see_raw_data.lower() in raw_data_ans
        except:
            print("Wrong answer. Enter yes or no\n")
            continue
        else:
            break
    count = 0
    if wants_to_see_raw_data == "yes":
        five_rows = next(dataframe_gen)
        print("The first five rows of the data are:\n")
        print(f"{five_rows}")
        count += nrows
        while count <= len(dataframe):
            next_five_rows = next(dataframe_gen)
            try:
                next_five_rows_ans = input("Do you want to see the next five rows?. yes or no\n")
                assert next_five_rows_ans in raw_data_ans
            except:
                print("Wrong answer. Enter yes or no\n")
                continue
            else:
                if next_five_rows_ans == "yes":
                    print("The next five rows of the data are:\n")
                    print(f"{next_five_rows}")
                    count += nrows
                else:
                    break
            



def format_hour(hour):
    """
    Format hour in a more human friendly manner
    """
    if hour == 0:
        return str(hour) + " AM"
    if hour >=1 and hour < 11:
        return str(hour) + " AM"
    if hour == 12:
        return str(hour) + " PM"
    return str(hour - 12) + " PM"

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ["chicago", "new york city", "washington"] 
    while True:
        try:
            city = input(f"Would you like to see data for chicago, new york city, or washington?\n")
            assert city.lower() in cities
        except:
            print(f"Wrong Input. City must be a string element from {cities}\n")
            continue
        else:
            city = city.lower()
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            filter_ans = int(input(f"Would you like to filter the data by month, day, or not at all? \nEnter 1 To filter the data by month, 2 to filter the data by day, and 3 to see all the data ?\n"))
            assert filter_ans in filter_options
        except:
            print(f"Invalid choice. Your answer should be either 1, 2 or 3\n")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_ans == 1:
        while True:
            try:
                month = input("Which month - January, February, March, April, May, or June?\n")
                assert month.capitalize() in months
            except StopIteration:
                print("Nothing to print anymore")
                break
            except:
                print(f"Invalid Input. the month must be one of {months}\n")
                continue
            else:
                month = months.index(month.capitalize()) + 1
                day = "all"
                break
    elif filter_ans == 2:
        while True:
            try:
                day = input(f"Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")
                assert day.capitalize() in days
            except:
                print(f"Invalid Input. the day must be one of {days}\n")
                continue
            else:
                day = days.index(day.capitalize())
                month = "all"
                break
    else:
        month = "all"
        day = "all"

    #print(city, month, day)
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['End Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    
    if month != "all" and day == "all":
        return df[df['Start Time'].dt.month == month]
    elif month == "all" and day != "all":
        return df[df['Start Time'].dt.dayofweek == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = months[int(df['Start Time'].dt.month.mode()) -1]
    print(f"The most common month is {month}")

    # display the most common day of week
    day = days[int(df['Start Time'].dt.dayofweek.mode())]
    print(f"The most common day is {day}")

    # display the most common start hour
    hour = int(df['Start Time'].dt.hour.mode())
    hour_format = format_hour(hour)
    print(f"The most common hour is {hour_format}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    nb_start_trips = df['Start Station'].value_counts()[start_station]
    print(f'The most commonly used start station is {start_station} with {nb_start_trips} start station trips')


    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    nb_end_trips = df['End Station'].value_counts()[end_station]
    print(f'The most commonly used end station is {end_station} with {nb_end_trips} end station trips')


    # display most frequent combination of start station and end station trip
    comb_start_end_station = df.groupby(['Start Station', 'End Station'])['Trip Duration']
    freq_start_end_station = comb_start_end_station.count().idxmax()
    nb_comb = comb_start_end_station.count().max()
    print(f"The most most frequent combination of start station and end station trip is {freq_start_end_station} with a total of {nb_comb} trips")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'The total travel time is {total_travel_time} seconds')


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'The mean travel time is {mean_travel_time} seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    user_count_dict = dict(df['User Type'].value_counts())
    print("The counts of user types are:")
    for user, count in user_count_dict.items():
        print(f"{user} with {count} users" )
   
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count_dict = dict(df['Gender'].value_counts())
        print("The counts of gender are:")
        for gender, count in gender_count_dict.items():
            print(f"{gender} with {count} users" )
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year_of_birth = int(df['Birth Year'].min())
        most_recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].mode())
        print(f"The earliest year of birth is {earliest_year_of_birth}")
        print(f"The most recent year of birth is {most_recent_year_of_birth}")
        print(f"The most common year of birth is {most_common_year_of_birth}")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df, 5)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
