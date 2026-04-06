import pandas as pd



CSVColumns = [['id', 'name', 'dock_count', 'installation_date'],
                ['id', 'lat', 'long', 'city'],
                ['status_id','station_id', 'time', 'bikes_available', 'docks_available'],
                ['id', 'bike_id', 'duration', 'start_station_id', 'end_station_id', 'start_date', 'end_date'],
                ['bike_id', 'user_type', 'member_birth_year','member_gender'],
                ['date', 'max_temperature_f', 'min_temperature_f', 'max_visibility_miles', 'events']]
#Take a master csv file and convert it to
#station.csv, station_location.csv, status.csv, weather.csv, trip.csv, user.csv

# Multiple intake options: 
# # trim smaller csv files to what is needed

# Convert strings to integers or floats
def convertToNum(columnName, df):
    df[columnName] = pd.to_numeric(df[columnName], errors='coerce')
    
    #drop empty values and values that couldnt be converted to int
    df = df.dropna(subset=[columnName])
    
    return df

# Convert strings to mm/dd/yyyy and HH:MM:SS if needed
    # seconds is a boolean to check if seconds should be included or not
def convertToDate(columnName, df, seconds):
    df[columnName] = pd.to_datetime(df[columnName], errors='coerce')

    #drop empty values and values that couldnt be converted to int
    df = df.dropna(subset=[columnName])

    #Convert to mm/dd/yyyy with or without hr:min:sec
    if seconds:
        df[columnName] = df[columnName].dt.strftime('%m/%d/%Y %I:%M:%S')
    else:
        df[columnName] = df[columnName].dt.strftime('%m/%d/%Y')
    return df

def emptyToNaN(columnName, df):
    df[columnName] = df[columnName].replace('', pd.NA)
    return df
    


def cleanData(filePath, userInput):
    
    #Convert CSV into a data frame
    rawPath = "raw_data/" + filePath
    df = pd.read_csv(rawPath, engine='pyarrow')
    
    #Case to create a new column for primary key
    primaryKeyIndex = []
    

    #Remove column if its not used in database
    for columnName, content in df.items():
        if not(columnName in CSVColumns[userInput]):
            df.drop([columnName], axis=1)
    
    
    #Case to create a new column for primary key
    if userInput == 2:
        primaryKeyIndex.extend(range(0,len(df)))
        df.insert(0,'status_id',primaryKeyIndex)

    #Clean Data
    match userInput:
        case 0:
            df = convertToNum('id', df)
            #drop duplicate values
            df = df.drop_duplicates(subset=['id'])

            df = emptyToNaN('name', df)
            df = convertToNum('dock_count', df)
            df = convertToDate('installation_date', df, False)
        case 1:
            df = convertToNum('id', df)
            df = df.drop_duplicates(subset=['id'])

            df = convertToNum('lat', df)
            df = convertToNum('long', df)
            df = emptyToNaN('city', df)
        case 2:
            df = convertToNum('station_id', df)
            df = df.drop_duplicates(subset=['station_id'])
            df = convertToDate('time', df, True)

            df = convertToNum('bikes_available', df)
            df = convertToNum('docks_available', df)
        case 3:
            df = convertToNum('id', df)
            df = df.drop_duplicates(subset=['id'])
            
            df = convertToNum('bike_id', df)
            df = convertToNum('duration', df)
            df = convertToNum('start_station_id', df)
            df = convertToNum('end_station_id', df)
            df = convertToDate('start_date', df, True)
            df = convertToDate('end_date', df, True) 
            
            
            #filter to only bike_id's in User.csv
            dfUser = pd.read_csv('clean_data/User.csv', engine='pyarrow')
            df = df[df['bike_id'].isin(dfUser['bike_id'])]

            #filter to only station_id's in station.csv
            dfStation = pd.read_csv('clean_data/station.csv', engine='pyarrow')
            df = df[df['start_station_id'].isin(dfStation['id'])]
            df = df[df['end_station_id'].isin(dfStation['id'])]
        case 4:
            df = convertToNum('bike_id', df)
            df = df.drop_duplicates(subset=['bike_id'])
            df = emptyToNaN('user_type', df)
            df = emptyToNaN('member_birth_year', df)
            df = emptyToNaN('member_gender', df)
        case 5:
            df = convertToDate('date', df, False)
            df = df.drop_duplicates(subset=['date'])

            df = convertToNum('max_temperature_f', df)
            df = convertToNum('min_temperature_f', df)
            df = convertToNum('max_visibility_miles', df)
            df = emptyToNaN('events', df)


    #reorder table
    df = df.loc[:, CSVColumns[userInput]]

    #connect weather to status
    if userInput == 2:
        df2 = df['time'].copy()
        df2 = df2.to_frame(name='date_with_time')

        df3 = df2['date_with_time'].copy()
        df3 = df3.to_frame(name='date_without_time')
        df3 = convertToDate('date_without_time', df3, False)
        
        df4 = pd.DataFrame()
        df4['date_with_time'] = df2['date_with_time'].copy()
        df4['date_without_time'] = df3['date_without_time'].copy()
        df4 = df4.drop_duplicates()
        df4.to_csv('clean_data/connect_Weather_Status.csv', index=False)

        #filter to only bike_id's in User.csv
        dfUser = pd.read_csv('clean_data/connect_Weather_Status.csv', engine='pyarrow')
        df = df[df['time'].isin(dfUser['date_with_time'])]
        



    #rewrite old csv with new one
    if (userInput == 1):
        filePath = 'station_location.csv'



    cleanPath = 'clean_data/' + filePath
    df.to_csv(cleanPath, index=False)




#Have User choose which CSV to clean for loading
print("Which CSV do you wish to clean\nstation (1)\nstation_location (2)\nstatus (3)")
print("trip (4)\nuser (5)\nweather(6)\nall (7)")

userInput = int(input(">> "))
match userInput:
    case 1:
        filePath = 'station.csv'
    case 2:
        filePath = 'station.csv'
    case 3:
        filePath = 'status.csv'
    case 4:
        filePath = 'trip.csv'
    case 5:
        filePath = 'User.csv'
    case 6:
        filePath = 'weather.csv'
    case 7:
        filePath = 'not needed'
    case _:
        print("Incorrect input")

if userInput > 0 and userInput < 7:
    cleanData(filePath, userInput - 1)
elif userInput == 7:
    cleanData('station.csv', 0)
    cleanData('station.csv', 1)
    cleanData('User.csv', 4)
    cleanData('trip.csv', 3)
    cleanData('weather.csv', 5)
    cleanData('status.csv', 2)