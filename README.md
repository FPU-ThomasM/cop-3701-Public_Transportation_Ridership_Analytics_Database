# cop-3701-Public_Transportation_Ridership_Analytics_Database

**Scope**: Database designed to easily show the routes taken by different users and the time when said routes are taken to help clearly show which areas are most popular at which different points of time and determine when is the peak hours for bike share buisnesses.

**Database Application**: Datagrip

**Users**: Bike Share Companies

**Data Sources**
- https://www.kaggle.com/datasets/benhamner/sf-bay-area-bike-share
- https://www.kaggle.com/datasets/jolasa/bay-area-bike-sharing-trips

**How to Use**: 
- Load raw data into the raw_data folder
- Run preprocess.py to have the data be cleaned. Clean data is stored in clean_data
- Open app.py and edit DB_USER, DB_PASS, and DB_DSN to your database
- To launch app.py run the command python -m streamlit run app.py

**ER Diagram**
![ER Diagram](https://github.com/FPU-ThomasM/cop-3701-Public_Transportation_Ridership_Analytics_Database/blob/main/finalized%20er%20diagram.png?raw=true)
