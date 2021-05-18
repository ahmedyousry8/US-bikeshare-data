import pandas as pd
import time
"""get_filters function is defined to take inputs of user and return these inputs to load the proper city data and to filter data"""
"""filter_data applies the user preferences to the data"""
"""result is the final step in which stats are calculated and outputs are printed to user"""
def run_program():
    CITY_DATA = { 'chicago': 'chicago.csv',
                  'new york city': 'new_york_city.csv',
                  'washington': 'washington.csv' }
    print('Hello! Let\'s explore some US bikeshare data!')
    def get_filters():
        valid_city = ["chicago", "new york city", "washington",'all']
        valid_month= ["1","2",'3','4','5','6','all']
        valid_day= ["saturday",'sunday','monday','tuesday','wednesday','thursday','friday','all']
        """while loop to prompt the user to enter a valid inputs"""
        x= True
        y= True
        z=True
        city= input('please choose a city( chicago, new york city, washington or all) to analyze: ').lower()
        while x:
            if city in valid_city:
                break
            else:
                city= input('please enter a valid city: ').lower()
                x=True
        month= input('please choose a month(from the first 6 months)(enter month in numerical form or all for all months): ').lower()
        while y:
            if month in valid_month:
                break
            else:
                month= str(input('please enter a valid month: ')).lower()
                x=True

        day= input('please enter a day (saturday, sunday, monday, tuesday, wednesday, thursday, friday or all): ').lower()
        while z:
            if day in valid_day:
                break
            else:
                day=input('please enter a valid day: ').lower()
                z=True
        print('Chosen city is:',city,'\n Chosen month is:' ,month,'\n Chosen day is:',day)
        return city,month,day
    city,month,day =get_filters()
    """while loop to confirm the user inputs"""
    t= True
    while t:
        error= input('Do you want to make changes? y/n: ')
        if error=="y":
            get_filters()
        else:
            t=False
            print('Please wait while getting data')
    print('\loading data...Please wait\n')
    start_time = time.time()
    def load_data(city, month, day):
        """reading the proper csv file and loading it into a dataframe"""
        city_csv_df= pd.read_csv(CITY_DATA[city])
        """converting start time column to datetime form readable by python"""
        city_csv_df['Start Time']= pd.to_datetime(city_csv_df['Start Time'])
        """creating new columns with data extracted from start time column, such as month,day,hour
        these new columns ease the filtering process according to user inputs"""
        city_csv_df['month']= city_csv_df['Start Time'].dt.month
        city_csv_df['day']= city_csv_df['Start Time'].dt.day_name()
        city_csv_df['hour']= city_csv_df['Start Time'].dt.hour
        city_csv_df['trip']= city_csv_df[['Start Station','End Station']].agg(' to '.join, axis=1)
        return city_csv_df
    city_csv_df= load_data(city,month,day)
    print("\nLoading data took %s seconds." % (time.time() - start_time))
    print('\Filtering data...\n')
    start_time = time.time()
    def filtered_data():
        """while loop to choose the proper code to run according to user input"""
        x=True
        while x:
            if month=="all" and day=="all":
                city_csv_df2=city_csv_df #no filter is applied
                break
            elif month =="all" and day!="all":
                filtered_city_data=city_csv_df.groupby(['day']) #filtering by day only
                city_csv_df2=filtered_city_data.get_group(day.title())
                break
            elif month!="all" and day=="all":
                filtered_city_data=city_csv_df.groupby(['month']) #filtring by month only
                city_csv_df2=filtered_city_data.get_group(int(month))
                break
            elif month!="all" and day!="all":
                filtered_city_data=city_csv_df.groupby(['month', 'day']) #filtring by both day and month
                city_csv_df2=filtered_city_data.get_group((int(month), day.title()))
                break
        return city_csv_df2
    city_csv_df3=filtered_data()
    print("\nFiltering data took %s seconds." % (time.time() - start_time))
    print('\nCalculating statistics...Please wait\n')
    start_time = time.time()
    def results():
        """a function to get the results"""
        most_common_month=city_csv_df3['month'].value_counts().idxmax()
        most_common_hour=city_csv_df3['hour'].value_counts().idxmax()
        most_common_distination=city_csv_df3['End Station'].value_counts().idxmax()
        most_common_start_station=city_csv_df3['Start Station'].value_counts().idxmax()
        most_common_trip=city_csv_df3['trip'].value_counts().idxmax()
        user_types=city_csv_df3.groupby(['User Type'])['User Type'].count()
        total_trip_time=city_csv_df3['Trip Duration'].sum()
        average_trip_time=city_csv_df3['Trip Duration'].mean()
        """if statement to account for the missing columns in washington data"""
        if city !='washington':
                user_gender= city_csv_df3.groupby(['Gender'])['Gender'].count()
                youngest_age=2021-city_csv_df3['Birth Year'].max()
                oldest_age=2021- city_csv_df3['Birth Year'].min()
                most_common_age=2021-city_csv_df3['Birth Year'].value_counts().idxmax()
        else:
                user_gender= "User gender is: Unavailable info"
                youngest_age="Unavailable info"
                oldest_age="Unavailable info"
                most_common_age="Unavailable info"
        print('Most common month is: ', most_common_month)
        print('-'*40)
        print('Most common time is: ', most_common_hour)
        print('-'*40)
        print('Most popular distination is: ',most_common_distination)
        print('-'*40)
        print('Most common start place is: ',most_common_start_station)
        print('-'*40)
        print('Most popular trip is: ', most_common_trip)
        print('-'*40)
        print(user_types)
        print('-'*40)
        print(user_gender)
        print('-'*40)
        print('Youngest age of user is: ',youngest_age)
        print('-'*40)
        print('Oldest age of user is: ',oldest_age)
        print('-'*40)
        print('Most travellers are of age: ',most_common_age)
        print('-'*40)
        print('Total trip time is: ',total_trip_time)
        print('-'*40)
        print('Average trip time is: ',average_trip_time)
    results()
    print("\nComputing results took %s seconds." % (time.time() - start_time))
    """while loop to ask user if he/she wants to run the program again"""

    b= True
    i=0
    while b:
        raw= input('Do you want to review some raw data? y/n: ')
        if raw=="y":
            print(city_csv_df.iloc[i:i+5])
            i+=5
        else:
            b=False
            a= True
            while a:
                """another nested while loop to ask if the user wants to run the code again"""
                again= input('Do you want to run program agian? y/n: ')
                if again=="y":
                    run_program()
                else:
                    a=False
                    b=False
                    print('Thank you for using our program')

run_program()
