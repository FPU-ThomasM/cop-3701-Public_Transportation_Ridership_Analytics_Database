import streamlit as st
import oracledb

# ----------------------------
# DATABASE SETUP
# ----------------------------
LIB_DIR = r"your_directory_path"
DB_USER = "your_username"
DB_PASS = "your_password"
DB_DSN = "your_dsn"


@st.cache_resource
def init_db():
    try:
        oracledb.init_oracle_client(lib_dir=LIB_DIR)
    except:
        pass


init_db()


def get_connection():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASS,
        dsn=DB_DSN
    )


# ----------------------------
# UI
# ----------------------------
st.title("Public Transportation Ridership Analytics Database App")

st.markdown("## Credits")

st.write("Database Designer: **Kallie Mendez**")
st.write("UI Developer: **Brandon Bachoco**")

st.markdown("## Data Sources")

st.markdown("""
- https://www.kaggle.com/datasets/benhamner/sf-bay-area-bike-share
- https://www.kaggle.com/datasets/jolasa/bay-area-bike-sharing-trips
""")

choice = st.selectbox("Choose a query", [
    "Trips with stations",
    "Trips per station",
    "Status",
    "Station Locations",
    "Bike usage per bike"
])

conn = get_connection()
cur = conn.cursor()


# ----------------------------
# 1. TRIPS WITH STATIONS
# ----------------------------
if choice == "Trips with stations":
    cur.execute("""
        SELECT t.TRIP_ID, s1.NAME, s2.NAME, t.DURATION
        FROM Trip t
        JOIN Station s1 ON t.START_STATION_ID = s1.STATION_ID
        JOIN Station s2 ON t.END_STATION_ID = s2.STATION_ID
    """)

    for row in cur.fetchall():
        st.write(row)


# ----------------------------
# 2. TRIPS PER STATION
# ----------------------------
elif choice == "Trips per station":
    cur.execute("""
        SELECT s.NAME, COUNT(*)
        FROM Station s
        JOIN Trip t ON s.STATION_ID = t.START_STATION_ID
        GROUP BY s.NAME
    """)

    for row in cur.fetchall():
        st.write(row)


# ----------------------------
# 3. STATUS
# ----------------------------
elif choice == "Status":
    cur.execute("""
        SELECT s.NAME, st.BIKES_AVAILABLE, st.DOCKS_AVAILABLE
        FROM Status st
        JOIN Station s ON s.STATION_ID = st.STATION_ID
    """)

    for row in cur.fetchall():
        st.write(row)


# ----------------------------
# 4. STATION LOCATIONS
# ----------------------------
elif choice == "Station Locations":

        cur.execute("""SELECT 
    s.NAME,
    l.CITY,
    l.LATITUDE,
    l.LONGITUDE
FROM Station s
JOIN Station_location l ON s.STATION_ID = l.STATION_ID
""")

        for row in cur.fetchall():
            st.write(row)


# ----------------------------
# 5. BIKE USAGE PER BIKE
# ----------------------------
elif choice == "Bike usage per bike":

        cur.execute("""
    SELECT 
    u.BIKE_ID,
    u.USER_TYPE,
    COUNT(t.TRIP_ID) AS total_trips
FROM "User" u
JOIN Trip t ON u.BIKE_ID = t.BIKE_ID
GROUP BY u.BIKE_ID, u.USER_TYPE
ORDER BY total_trips DESC
""")

        for row in cur.fetchall():
            st.write(row)


cur.close()
conn.close()