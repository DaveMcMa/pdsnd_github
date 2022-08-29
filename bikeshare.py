import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

valid_month_range = ['all','january','february','march','april','may','june']
valid_day_range = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # getting user input for city
    while True:
        city = input('Which cities data would you like to exlpore? (chicago / new york city / washington): ').lower()
        if city in CITY_DATA:
            print('input accepted \n')
            break
        else:
            print('we don\'t recognise that city, please try again and select either chicago, new york city or washington')
            continue

    # getting user input for month
    while True:
        month = input('For which month would you like to see data? (please select either "all" or a month between january and june): ').lower()
        if month in valid_month_range:
            print('input accepted \n')
            break
        else:
            print('we don\'t recognise that month, please select either "all" or a month between january and june')
            continue

    #getting user input for day
    while True: 
        day = input('Which day of the week would you like to see (select "all" or any day of the week): ').lower()
        if day in valid_day_range:
            print('input accepted \n')
            break
        else:
            print('we don\'t recognise that day, please try again and select either "all" or any day of the week')
            continue
    
    return city,month,day


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

    # transforming the data so we can apply our inputs correctly
    df = pd.read_csv(CITY_DATA.get(city)) #reading the correct file based on the city 
    df['Start Time'] = pd.to_datetime(df['Start Time']) # convert this column to 'datetime'
    df['month'] = df['Start Time'].dt.month # making new column with month (numerical)
    df['day_of_week'] = df['Start Time'].dt.weekday # making new column with day of week (numerical)
    df['hour'] = df['Start Time'].dt.hour # making new column with hour (does not require a filter later)
    
    # now lets apply our filters
    # filtering by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        print("integer of month: ", month)
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days.index(day) + 1
        print("integer of day: ", day)
        # filter by day to create the new dataframe
        df = df[df['day_of_week'] == day]
        
    return df

def display_raw_data(df):
    """Prompts user if they would like to see raw data from the series they have selected"""
    index=0
    cont='yes'
    
    while True:
        display = input('Would you like to see raw data first? (yes/no)').lower()
        if display=='yes':
            print('input accepted \n')
            while cont=='yes':
                    print(df.iloc[index:index+5], '\n')
                    index+=5
                    cont = input('Would you like to continue to the next 5 lines of raw data? (yes / any other input): ')
            print('OK, proceeding to statistics now: ')
            break
        elif display=='no':
            print('input accepted \n')
            print('OK, proceeding to statistics now: ')
            break
        else:
            print('we don\'t recognise that input, please select yes or no!')
            continue
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()
    
    print('\nCalculating The Most Frequent Times of Travel...\n')

    # display the most common month
    print('The most popular month from this dataset: ', valid_month_range[df['month'].mode()[0]])
    
    # display the most common day of week
    print('The most popular day of the week from this dataset: ', valid_day_range[df['day_of_week'].mode()[0]])
    
    # display the most common start hour
    print('The most popular starting hour from this dataset: ', df['hour'].mode()[0])

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most popular start station from this dataset: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most popular end station from this dataset: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False) 
    print('The most frequent combination of start and end station: ', combination.index[0]) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('the total time travelled during this dataset was: ',df['Trip Duration'].sum())

    
    # display mean travel time
    print('the mean time travelled during this dataset was: ',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The count of user-types was as follows \n')
    print(df['User Type'].value_counts(), '\n')

    # Display counts of gender (include exception for cities that don't have this data)
    while True:
        try:
            print('The gender count from available data was as follows \n', df['Gender'].value_counts(), ' \n')
            break
        except KeyError:
            print("Gender information is not available from this city \n")
            break
               
    # Display earliest, most recent, and most common year of birth (include exception for cities that don't have this data)
    while True:
        try:
            print('The earliest year of birth of a service-user was: ', int(df['Birth Year'].min()))
            print('The most recent year of birth of a service-user was: ', int(df['Birth Year'].max()))
            print('The most common year of birth of a service-user was: ', int(df['Birth Year'].mode()[0]))
            break
        except KeyError:
            print('Date of Birth information is not available for this city')
            break
            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
