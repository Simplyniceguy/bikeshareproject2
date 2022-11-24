import time
import pandas as pd
import numpy as np
import datetime as dt
from statistics import mode
from collections import Counter


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters(): 
    cities=['Chicago', 'New York City', 'Washington']
    months=['January', 'February', 'March', 'April', 'June', 'May', 'None']
    days=['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday', 'None']
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    

    city=input("\n What city would you like to discuss?  (Chicago, New York City, Washington) \n").title()
    print(city)
    
    while city not in cities:
        city=input("\n Please enter an actual city's name. Choose from Chicago, New York City, Washington\n").title()   
        print('nope')
    else: 
        month=input("\n Which month would you like to discuss?  (January, February, March, April, May, June) Type 'None' for no month filter\n").title()
        print(month)
        
    while month not in months:
        month=input("\n Please enter an actual month.  Choose from January, February, March, April, May, June, or None \n").title()
        print('nope')
    else: 
        day =input("\n What day would you like to discuss? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Type 'None' if you would not like to assess by day \n").title()
        print(day)
            
            
    while day not in days:
        day = input("\n Please enter an actual day. Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or None \n").title()
        print('nope')
    else: 
        print('Thank You.  Now we can proceed')    

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
    print(df.head())
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    
    print("month is {}".format(month))
    if month != 'None':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1
        print("months.index(month) is {}".format(month))
        
        df = df[df['month']== month]
        print("df.Month = {}".format(month))
    
    print("day is {}".format(day))
    print(df.head())
    if day != 'None':
        days = ['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday', 'None']
        day = days.index(day)+1
        print("days.index(day) is {}".format(day)) 
        
        df = df[df['day_of_week']== day]
        print ("df.day_of_week = {}".format(day))          
    print(df.head())
    return df
    
 
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start time']=pd.to_datetime(df['Start Time'])
    
  
    print(df.head())
    most_popular_month = df['month'].mode()[0]
    print ("The most common travel month is: ", most_popular_month)
    
    most_popular_weekday = df['day_of_week'].mode()[0]
    print ("The most common travel day is {}.\r\n".format(most_popular_weekday))
    
    df['hour']=df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print ("The most common start hour is {}.\r\n".format(most_popular_hour))
    
    print("\nThis took %s seconds." %(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()
    
    
    # display most commonly used start station
    common_start_station= df['Start Station'].value_counts().idxmax()
    print("The most commonly used Start Station is {}".format(common_start_station))

    # display most commonly used end station
    common_end_station= df['End Station'].value_counts().idxmax()
    print("The most commonly used End Station is {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    df['Start End']= df['Start Station'].map(str) + 'and' + df['End Station']
    common_station_combintion=df['Start End'].value_counts().idxmax()
    print("\nThe most common combination of Start and End Stations is:  ", common_start_station, "and", common_end_station)
                                                           

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration=sum(df['Trip Duration'])
    print('Total travel duration: ', total_duration/86400, 'days')

    # display mean travel time
    avg_duration=df['Trip Duration'].mean()
    print ('Mean Travel Time: ', avg_duration/60, 'minutes')
                                                           
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    biker_counts=df['User Type'].value_counts()
    print("The user types are:\n",biker_counts)
    
    # Display counts of gender
    if city.title() == 'Chicago' or city.title() == 'New York City':
        gender_counts=df['Gender'].value_counts()
        print("\nThe gender counts are:\n",gender_counts)                                                           
    # Display earliest, most recent, and most common year of birth
        earliest= int(df['Birth Year'].min())
        print("\nThe oldest user was born in ",earliest)
        most_recent= int(df['Birth Year'].max())
        print("The youngest user was born in",most_recent)
        most_common= int(df['Birth Year'].mode()[0])
        print("Most users were born in the year",most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def rawdata(df):
    raw_data = input('\nWould you like to see more raw data?  Enter yes or no.\n')
    while raw_data.lower() == 'yes':
        print ('\nRetrieving raw data\n')
        print (df.head(5))
        raw_data = input('\nWould you like to see more raw data?  Enter yes or no.\n')
    else:
        print ('\nStopping data retrieval\n')
         
        
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        rawdata(df)

        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
