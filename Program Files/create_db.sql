Create User Bike_Share identified by "bikeShare123";
Grant DBA to Bike_Share;

-- Create Tables
Create TABLE Station (
    station_id int primary key,
    name varchar(50) not null,
    dock_count int,
    installation_date date not null
);

Create TABLE Station_location (
    station_id int primary key,
    Latitude float not null,
    Longitude float not null ,
    City varchar(50) not null
);

Create TABLE Status (
    status_id int primary key,
    station_id int,
    time date,
    bikes_available int,
    docks_available int
);

Create table weather (
    "Date" date primary key,
    Max_temp_f float(1),
    Min_temp_f float(1),
    max_vis_miles float(1),
    events varchar(20)
);

Create TABLE "User" (
    Bike_ID int primary key,
    user_type varchar(10),
    user_birth_year int,
    user_gender varchar(6)
);

Create Table Trip(
    trip_id int primary key ,
    bike_id int not null ,
    duration int not null ,
    start_station_id int not null ,
    end_station_id int not null ,
    start_date date not null ,
    end_date date not null
);

--Implement Foreign Keys
Alter TABLE Station_location
    Add Constraint station_id
        FOREIGN KEY (station_id)
        references Station(station_id);
Alter TABLE Status
    Add CONSTRAINT status_station_id
        foreign key (station_id)
        references station(station_id)
    Add CONSTRAINT time
        foreign key (time)
        references weather("Date");
Alter Table Trip
    Add CONSTRAINT start_station_id
        foreign key (start_station_id)
        references Station(station_id)
    Add constraint end_station_id
        foreign key (end_station_id)
        references Station(station_id)
    Add constraint start_date
        foreign key (start_date)
        references weather("Date")
    Add constraint end_date
        foreign key (end_date)
        references weather("Date")
    Add constraint trip_bike_id
        foreign key (bike_id)
        references "User"(Bike_ID);
