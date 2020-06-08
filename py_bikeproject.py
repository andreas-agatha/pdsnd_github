import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = CITY_DATA.keys()
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
weekdays = ['monday','tuesday','wednesday','thursday','friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hi there! Thanks for your interest in US bikeshare data insights!")
    print()
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Which city would you like to explore bikeshare data for?")
    print("Data sets for Chicago, New York City and Washington are currently available.")
    print("Type any of the available cities in given spelling, without quotation marks (''):")
    city = input('Choose city: ').lower()

    while city not in cities:
        print("Incorrect entry, please re-enter city in given spelling...")
        city = input('Choose city: ').lower()
        if city in cities:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    print("Data entry for city successful.")
    print()
    print("Now please specify which month you would like to see data for, datasets from January to June are currently available.")
    print("Choose from {} in given spelling, without quotation marks ('').".format(months))
    month = input('Choose month: ').lower()

    while month not in months:
        print("Incorrect entry, please re-enter month in given spelling...")
        month = input('Choose month: ').lower()
        if month in months:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print("Data entry for month successful.")
    print()
    print("Now please specify if you would like to engage a day of week data filter.")
    print("Choose from {} in given spelling, without quotation marks ('').".format(weekdays))
    day = input('Choose day: ').lower()

    while day not in weekdays:
        print("Incorrect entry, please re-enter day in given spelling...")
        day = input('Choose day: ').lower()
        if day in weekdays:
            break

    print('-'*40)
    print("Data entry completed. Data will be provided for city '{}', month '{}' and day filter '{}'.".format(city, month, day))
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

    # Data for Pandas DataFrame
    df = pd.read_csv(CITY_DATA[city])
    df.dropna(axis=0)

    # Start time conversion
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Derive month and day in DataFrame in new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek

    # month filter
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # day filter
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        day = days.index(day)
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print("The most common rental month is {}, with 1=January and 6=June.".format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day'].mode()[0]
    print("The most common rental day is {}, with 1=Monday and 7=Sunday.".format(common_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("The most common start hour for the selected data filter is {}:00 am/pm.".format(common_hour))
    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station in the selected timeframe is {}.".format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station in the selected timeframe is {}.".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['station_combined'] = df['Start Station'] + ' and ' + df['End Station']
    station_comb = df['station_combined'].mode()[0]
    print("The most frequent combination of start and end station is {}.".format(station_comb))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = (df['Trip Duration'].sum()) /60
    total_travel_hours = total_travel_time / 60
    print("The total trip duration is {} minutes = {} hours.".format(total_travel_time, total_travel_hours))
    # TO DO: display mean travel time
    mean_travel_time = (df['Trip Duration'].mean()) /60
    print("The mean/average trip duration is {} minutes.".format(mean_travel_time))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    usertype_count = df['User Type'].value_counts()
    print("Usertype distribution: \n{}".format(usertype_count))
    print()

    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print("Total gender distribution: \n{}.".format(gender_count))
        print()
    except:
        print("Gender stats not available in filtered city dataset.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        avg_birth = df['Birth Year'].mode()[0]
        oldest_birth = df['Birth Year'].min()
        youngest_birth = df['Birth Year'].max()
        print("The average user birth year is: {}".format(avg_birth))
        print("The oldest user birth year is: {}".format(oldest_birth))
        print("The youngest user birth year is: {}".format(youngest_birth))
    except:
        print("Age/birth year stats not available in filtered city dataset.")

    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_data(df):
    """ Displays individual raw data on the users' request """
    print("\nWould you like to see some raw data for the statistics as calculated above? yes/no")
    user_choice = input("Enter yes/no: ").lower()
    print()
    show_data = 5
    while user_choice == 'yes':
        print(df.iloc[show_data - 5:show_data])
        show_data += 5
        print("\nWould you like to see more data? yes/no")
        user_choice = input("Enter yes/no: ").lower()
        if user_choice != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
