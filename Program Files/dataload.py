#load csv file from data folder and upload it into the database
import oracledb
import csv

# --- SETUP ---
LIB_DIR = r"C:\Users\screa\Desktop\College\Year 2\Spring\Databases\Project\Program Files\instantclient-basiclite-windows.x64-23.26.1.0.0\instantclient_23_0"  # Your Instant Client Path
DB_USER = "Bike_Share"
DB_PASS = "bikeShare123"
DB_DSN  = "127.0.0.1:1521/xe"

# Initialize Thick Mode (Required for FreeSQL/Cloud)
oracledb.init_oracle_client(lib_dir=LIB_DIR)

#Load python data
def bulk_load_csv(file_path, userInput):
    try:
        

        # 1. Connect
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()

        # 2. Read CSV Data into a List
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            data_to_insert = [row for row in reader]

        # 3. Prepare Bulk Insert SQL
        # :1 and :2 correspond to the values in each row of your list
        # userInput determines which command to run
        sql = "INSERT INTO "
        match userInput:
            case 1:
                sql += "station (station_id, name, dock_count, installation_date) VALUES (:1, :2, :3, TO_DATE(:4, 'mm/dd/yyyy'))"
            case 2:
                sql += "station_location (station_id, latitude, longitude, city) VALUES (:1, :2, :3, :4)"
            case 3:
                sql += "status (status_id, station_id, time, bikes_available, docks_available) VALUES (:1, :2, TO_DATE(:3, 'mm/dd/yyyy hh24:mi:ss'), :4, :5)"
            case 4:
                sql += "trip (trip_id, bike_id, duration, start_station_id, end_station_id, start_date, end_date) "
                sql += "VALUES (:1, :2, :3, :4, :5, TO_DATE(:6, 'mm/dd/yyyy hh:mi:ss'), TO_DATE(:7, 'mm/dd/yyyy hh:mi:ss'))"
            case 5:
                sql += "\"User\" (bike_id, user_type, user_birth_year, user_gender) VALUES (:1, :2, :3, :4)"
            case 6:
                sql += "weather (\"Date\", max_temp_f, min_temp_f, max_vis_miles, events) VALUES (TO_DATE(:1, 'mm/dd/yyyy'), :2, :3, :4, :5)"
            case 7:
                sql += "concatenateTimeFromDate (date_time, date_no_time) VALUES (TO_DATE(:1, 'mm/dd/yyyy hh:mi:ss'), TO_DATE(:1, 'mm/dd/yyyy'))"
            case _:
                print ("Error: improper input given")

        

        # 4. Execute Batch
        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)
        
        # 5. Commit Changes
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")

    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback() # Undo changes if an error occurs

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


print("Which CSV do you wish to load\nstation (1)\nstation_location (2)\nstatus (3)")
print("trip (4)\nuser (5)\nweather(6)\nconnect weather status (7)\n all(8)")

userInput = int(input(">> "))


filePath = ""
match userInput:
    case 1:
        filePath = 'clean_data/station.csv'
    case 2:
        filePath = 'clean_data/station_location.csv'
    case 3:
        filePath = 'clean_data/status.csv'
    case 4:
        filePath = 'clean_data/trip.csv'
    case 5:
        filePath = 'clean_data/user.csv'
    case 6:
        filePath = 'clean_data/weather.csv'
    case 7:
        filePath = 'clean_data/connect_Weather_Status.csv'
    case _:
        print("unknown case")

if userInput != 8:
    bulk_load_csv(filePath, userInput)
elif userInput == 8 :
    bulk_load_csv('clean_data/station.csv', 1)
    bulk_load_csv('clean_data/station_location.csv', 2)
    bulk_load_csv('clean_data/user.csv', 5)
    bulk_load_csv('clean_data/trip.csv', 4)
    bulk_load_csv('clean_data/weather.csv', 6)
    bulk_load_csv('clean_data/connect_Weather_Status.csv', 7)
    bulk_load_csv('clean_data/status.csv', 3)
