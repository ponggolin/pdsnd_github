# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 11:47:50 2018

@author: jason
"""

import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

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
    while True:
        city = input("Select a city from {}, {} or {}:\n".format(*CITY_DATA.keys())).strip().lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("You enter the wrong input!\nPlease enter 'chicago' or 'new york city' or 'washington'.")
            
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month do you want to filter?\nPlease enter a month between January and June, or 'all' for no filter.\n").lower()
        if month in months:
            break
        else:
            print("You enter the wrong input!\nPlease enter a month between January and June, or 'all' for no filter.\n")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day do you want to filter?\nPlease enter a day between Monday and Sunday, or 'all' for no filter.\n").lower()
        if day in days:
            break
        else:
            print("You enter the wrong input!\nPlease enter a day between Monday and Sunday, or 'all' for no filter.\n")

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week an hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':      
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
                    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is: ', most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is: ', most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is: ', most_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print('The most commonly usded start station is: ', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print('The most commonly usded end station is: ', most_common_end_station)

    # display most frequent combination of start station and end station trip
    combo_station = df['Start Station'] + ' to ' + df['End Station']
    most_combo_station = combo_station.value_counts().idxmax()
    print('The most frequent combination of start station and end station trip is: ', most_combo_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: {} seconds'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: {} seconds'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type)

    # Display counts of gender
    if 'Gender' in df.columns:
        counts_of_gender = df['Gender'].value_counts()
        print('\n', counts_of_gender)    

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year_of_birth = df['Birth Year'].min()
        most_recent_year_of_birth = df['Birth Year'].max()
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        
        print('\nThe earliest year of birth: ', int(earliest_year_of_birth))
        print('The most recent year of birth: ', int(most_recent_year_of_birth))
        print('The most common year of birth: ', int(most_common_year_of_birth))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    # Ask for user input, and display 5 rows of data each time if 'yes'
    user_input = input("Do you want to see raw data? Please enter 'yes' or 'no'.\n")
    number_of_data = 0
    
    while True:    
        if user_input.lower() == 'yes':
            print(df.iloc[number_of_data : number_of_data + 5])
            number_of_data += 5
            user_input = input("Do you want to see more raw data? Please enter 'yes' or 'no'.\n")
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()    