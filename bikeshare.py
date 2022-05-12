import time
import pandas as pd
import numpy as np
import os.path
from pathlib import Path

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = None
    month = None
    day = None
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Value control        
    try:
        while   (city not in ['chicago', 'new york city','new york', 'washington']):
                city = input('Please enter a city from list provided => chicago, new york city,new york, washington : ')
                print("\n")
                city=city.lower()
        else:
            if  city == "new york" or city == "new york city":
                city = "new york city" 
                city_element = city
                print("Ville : {} ".format(city))
                print("\n")
        
            if city != "new york" or city != "new york city":
                    for city_element, file in CITY_DATA.items():
                        if  city_element == city: 
                            print("Ville : {}  File: {}".format(city_element, file))
                            print("\n")   

        # get user input for month (all, january, february, ... , june)
        while   (month not in ['all', 'january','february', 'march', 'april', 'may','june','july','august','september','october','november','october','november','december']):
                month = input("Please choose a correct month would you like to filter (all, january, february, ... , june) : ")
                print("\n")
                month=month.lower()
        else:  
                if  month == "all" or month == "all" or month == "ALL":
                    month="all"
                    print("data will be loaded for {} month".format(month))
                    print("\n")
                else:
                    print("data will be loaded for {} only ".format(month))
                    print("\n")
                    
        
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while   (day not in ['all', 'monday','tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday']):
                day = input("For which day of week (all, monday, tuesday, ... sunday): ")
                print("\n")
                day=day.lower()
        else:        
                if  day == "all" or day == "all" or day == "ALL":
                    day ="all"
                    print("data will be loaded for {} day".format(day))
                    print("\n")
                else:
                    print("data will be loaded for {} only ".format(day))
                    print("\n")
    except ValueError:
           print("Please enter a city from list provided ")
        
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
    for city_element, file in CITY_DATA.items():
            if  city_element == city: 
                print("Loading data for {} using File: {}".format(city_element, file))
                print("\n")
                #load data file into a dataframe
                df = pd.read_csv(file)
                #df = pd.read_csv(CITY_DATA[city])
                #convert the Start Time column to datetime
                df['Start Time'] = pd.to_datetime(df['Start Time'])
                #Extract the month and day of week from Start Time to create a new columns
                df['month'] = df['Start Time'].dt.month
                df['day_of_week'] = df['Start Time'].dt.day_name()
                # filter by month if applicable
                if month != 'all':
                    # use the index of the months list to get the corresponding int
                    months = ['january', 'february', 'march', 'april', 'may', 'june']
                    month = months.index(month) + 1

                    # filter by month to create the new dataframe
                    df = df[df['month'] == month]
                # filter by day of week if applicable
                if day != 'all':
                    # filter by day of week to create the new dataframe
                    df = df[df['day_of_week'] == day.title()]
    return df
  

def display_data(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nDisplaying the data retrieved from user input...\n')

    # display the most common month
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 5
    while view_data.lower() in ('yes' or 'y'):
        
        print(df.iloc[0:start_loc])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
        if view_data.lower() == 'no' or view_data.lower() == 'n':
         break

  
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    num_month = df['month'].mode()
    common_month = pd.to_datetime(num_month, format='%m').dt.month_name()
    print("Display most common month: " + common_month)
    
    # display the most common day of week
    common_dow = df['day_of_week'].mode()
    print("Display the most common day of week: " + common_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()
    print("Display the most common start hour: {}".format(common_hour))
    
    #print(df['hour'].mode())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()
    print("Common Start Station: " + common_start_station)
    #print(df['Start Station'])
    # display most commonly used end station
    common_end_station = df['End Station'].mode()
    print("Common End Station: " + common_end_station)
    #print(df['End Station'])

    # display most frequent combination of start station and end station trip
    df_new = df[['Start Station', 'End Station']]
    common_station = df_new.mode()
    #common_station = (' Start Station => ' + df['Start Station'] + '  End Station => ' + df['End Station']).mode()
    print("Common for Start and end Station: \n {}".format(common_station))
    #print(common_station)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def trip_duration_stats(city, month, df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total duration trip for {} in  {} month = {}".format(city, month,total_time))
    
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean duration trip for {} in  {} month = {}".format(city, month,mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
  
  
def user_stats(city,df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].count()
    print("count of User type total: {}".format(user_count))
    print("\n")
    user_count_per_type = df.groupby(['User Type'])['User Type'].count()
    print("count of User per {}".format(user_count_per_type))
    print("\n")
 
    if city != 'washington':
        # Display counts of gender
        gender_count = df['Gender'].count()
        print("count of Gender total: {}".format(gender_count))
        print("\n")
        gender_count_per_type = df.groupby(['Gender'])['Gender'].count()
        print("count of User per {}".format(gender_count_per_type))
        print("\n")
        # Display earliest, most recent, and most common year of birth
        most_earliest_year = df['Birth Year'].sort_values().head(1)
        print("Earliest year of birth : {}".format(most_earliest_year))
        print("\n")
    
        most_recent_year = df['Birth Year'].sort_values(ascending=False).head(1)
        print("Most recent year of birth : {}".format(most_recent_year))
        print("\n")
    
        #most_recent_year = df.groupby(['Birth Year'])['Birth Year'].count().nlargest()
        most_recent_year = df.groupby(['Birth Year'])['Birth Year'].count().sort_values(ascending=False)
        print("Most common year of birth : {}".format(most_recent_year.head(1)))
        print("\n")
    else:
        print("\n")
        print("No Gender & No year of birth calculated for {} city".format(city.title()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(city, month,df)
        user_stats(city,df)        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()