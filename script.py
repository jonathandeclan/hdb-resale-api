import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

query_string='https://data.gov.sg/api/action/datastore_search?resource_id=42ff9cfe-abe5-4b54-beda-c88f9bb438ee&limit=500'
resp = requests.get(query_string)

#Convert JSON into Python Object 
data = json.loads(resp.content)

# Checking the length of dataframe
len(data['result']['records'])

# Checking the length of dataframe
len(data['result']['records'])

town = []
flat_type = []
flat_model = []
floor_area_sqm = []
street_name = []
resale_price = []
month = []
remaining_lease = []
lease_commence_date = []
storey_range = []
_id = []
block = []

for i in range(0, len(hdb_price_dict_records)):
    town.append(hdb_price_dict_records[i]['town'])
    flat_type.append(hdb_price_dict_records[i]['flat_type'])
    flat_model.append(hdb_price_dict_records[i]['flat_model'])
    floor_area_sqm.append(hdb_price_dict_records[i]['floor_area_sqm'])
    street_name.append(hdb_price_dict_records[i]['street_name'])
    resale_price.append(hdb_price_dict_records[i]['resale_price'])
    month.append(hdb_price_dict_records[i]['month'])
    remaining_lease.append(hdb_price_dict_records[i]['remaining_lease'])
    lease_commence_date.append(hdb_price_dict_records[i]['lease_commence_date'])
    storey_range.append(hdb_price_dict_records[i]['storey_range'])
    _id.append(hdb_price_dict_records[i]['_id'])
    block.append(hdb_price_dict_records[i]['block'])
    
df_hdb_price = pd.DataFrame({
    'town': town,
    'flat_type': flat_type,
    'flat_model': flat_model,
    'floor_area_sqm': floor_area_sqm,
    'street_name': street_name,
    'resale_price': resale_price,
    'month': month,
    'remaining_lease': remaining_lease,
    'lease_commence_date': lease_commence_date,
    'storey_range': storey_range,
    '_id': _id,
    'block': block
})

# Let's examine our dataframe
df_hdb_price.head()

# First let's create a list of all the MRT stations in Singapore. 
# Since MRT stations change relatively slowly overtime, we can leverage a static list. 
# I obtained the data from Wikipedia, which also provides data on upcoming MRT stations.
# We will only consider existing MRT stations for now.
list_of_mrt = [
    'Jurong East MRT Station',
    'Bukit Batok MRT Station',
    'Bukit Gombak MRT Station',
    'Choa Chu Kang MRT Station',
    'Yew Tee MRT Station',
    'Kranji MRT Station',
    'Marsiling MRT Station',
    'Woodlands MRT Station',
    'Admiralty MRT Station',
    'Sembawang MRT Station',
    'Canberra MRT Station',
    'Yishun MRT Station',
    'Khatib MRT Station',
    'Yio Chu Kang MRT Station',
    'Ang Mo Kio MRT Station',
    'Bishan MRT Station',
    'Braddell MRT Station',
    'Toa Payoh MRT Station',
    'Novena MRT Station',
    'Newton MRT Station',
    'Orchard MRT Station',
    'Somerset MRT Station',
    'Dhoby Ghaut MRT Station',
    'City Hall MRT Station',
    'Raffles Place MRT Station',
    'Marina Bay MRT Station',
    'Marina South Pier MRT Station',
    'Pasir Ris MRT Station',
    'Tampines MRT Station',
    'Simei MRT Station',
    'Tanah Merah MRT Station',
    'Bedok MRT Station',
    'Kembangan MRT Station',
    'Eunos MRT Station',
    'Paya Lebar MRT Station',
    'Aljunied MRT Station',
    'Kallang MRT Station',
    'Lavender MRT Station',
    'Bugis MRT Station',
    'Tanjong Pagar MRT Station',
    'Outram Park MRT Station',
    'Tiong Bahru MRT Station',
    'Redhill MRT Station',
    'Queenstown MRT Station',
    'Commonwealth MRT Station',
    'Buona Vista MRT Station',
    'Dover MRT Station',
    'Clementi MRT Station',
    'Chinese Garden MRT Station',
    'Lakeside MRT Station',
    'Boon Lay MRT Station',
    'Pioneer MRT Station',
    'Joo Koon MRT Station',
    'Gul Circle MRT Station',
    'Tuas Crescent MRT Station',
    'Tuas West Road MRT Station',
    'Tuas Link MRT Station',
    'Expo MRT Station',
    'Changi Airport MRT Station',
    'HarbourFront MRT Station',
    'Chinatown MRT Station',
    'Clarke Quay MRT Station',
    'Little India MRT Station',
    'Farrer Park MRT Station',
    'Boon Keng MRT Station',
    'Potong Pasir MRT Station',
    'Woodleigh MRT Station',
    'Serangoon MRT Station',
    'Kovan MRT Station',
    'Hougang MRT Station',
    'Buangkok MRT Station',
    'Sengkang MRT Station',
    'Punggol MRT Station',
    'Bras Basah MRT Station',
    'Esplanade MRT Station',
    'Promenade MRT Station',
    'Nicoll Highway MRT Station',
    'Stadium MRT Station',
    'Mountbatten MRT Station',
    'Dakota MRT Station',
    'MacPherson MRT Station',
    'Tai Seng MRT Station',
    'Bartley MRT Station',
    'Lorong Chuan MRT Station',
    'Marymount MRT Station',
    'Caldecott MRT Station',
    'Botanic Gardens MRT Station',
    'Farrer Road MRT Station',
    'Holland Village MRT Station',
    'one-north MRT Station',
    'Kent Ridge MRT Station',
    'Haw Par Villa MRT Station',
    'Pasir Panjang MRT Station',
    'Labrador Park MRT Station',
    'Telok Blangah MRT Station',
    'Bayfront MRT Station',
    'Bukit Panjang MRT Station',
    'Cashew MRT Station',
    'Hillview MRT Station',
    'Beauty World MRT Station',
    'King Albert Park MRT Station',
    'Sixth Avenue MRT Station',
    'Tan Kah Kee MRT Station',
    'Stevens MRT Station',
    'Rochor MRT Station',
    'Downtown MRT Station',
    'Telok Ayer MRT Station',
    'Fort Canning MRT Station',
    'Bencoolen MRT Station',
    'Jalan Besar MRT Station',
    'Bendemeer MRT Station',
    'Geylang Bahru MRT Station',
    'Mattar MRT Station',
    'Ubi MRT Station',
    'Kaki Bukit MRT Station',
    'Bedok North MRT Station',
    'Bedok Reservoir MRT Station',
    'Tampines West MRT Station',
    'Tampines East MRT Station',
    'Upper Changi MRT Station'
]

mrt_lat = []
mrt_long = []

for i in range(0, len(list_of_mrt)):
    try:
        query_address = list_of_mrt[i]
        query_string = 'https://developers.onemap.sg/commonapi/search?searchVal='+str(query_address)+'&returnGeom=Y&getAddrDetails=Y'
        resp = requests.get(query_string)

        data_mrt=json.loads(resp.content)

        mrt_lat.append(data_mrt["results"][0]["LATITUDE"])
        mrt_long.append(data_mrt["results"][0]["LONGITUDE"])

        print (str(query_address)+",Lat: "+data_mrt['results'][0]['LATITUDE'] +" Long: "+data_mrt['results'][0]['LONGITUDE'])

    except:
        print ("Pausing for 15 Seconds")
        time.sleep(15)

# Store this information in a dataframe
mrt_location = pd.DataFrame({
    'MRT': list_of_mrt,
    'latitude': mrt_lat,
    'longitude': mrt_long
})

# Let's combine the block and street name to form the address of our transacted unit.
df_hdb_price['address'] = df_hdb_price['block'] + " " + df_hdb_price['street_name']

# Dedup Address List
df_dedup = df_hdb_price.drop_duplicates(subset='address', keep='first')
len(df_dedup)

# Next let's grab the unique addresses and create a list 
address_list = df_dedup['address'].tolist()
len(address_list)

# This may take a while...
latitude = []
longitude = []
blk_no = []
road_name = []
postal_code = []
address = []
count = 0

for row in range(len(address_list)):
    try:
        #formulate query string  
        query_address = address_list[row]
        query_string='https://developers.onemap.sg/commonapi/search?searchVal='+str(query_address)+'&returnGeom=Y&getAddrDetails=Y'
        resp = requests.get(query_string)          

        #Convert JSON into Python Object 
        data_geo_location=json.loads(resp.content)

        latitude.append(data_geo_location['results'][0]['LATITUDE'])
        longitude.append(data_geo_location['results'][0]['LONGITUDE'])
        blk_no.append(data_geo_location['results'][0]['BLK_NO'])
        road_name.append(data_geo_location['results'][0]['ROAD_NAME'])
        postal_code.append(data_geo_location['results'][0]['POSTAL'])
        address.append(query_address)
        print (str(query_address) + ",Lat: " + data_geo_location['results'][0]['LATITUDE'] + " Long: " + data_geo_location['results'][0]['LONGITUDE'])
    except:
        print ("Pausing for 15 Seconds")
        time.sleep(15)

# Fit into a dataframe
df_coordinates = pd.DataFrame({
    'latitude': latitude,
    'longitude': longitude,
    'blk_no': blk_no,
    'road_name': road_name,
    'postal_code': postal_code,
    'address': address
})
len(df_coordinates)

list_of_lat = df_coordinates['latitude']
list_of_long = df_coordinates['longitude']

# Creating a list of the coordinates
list_of_coordinates = []
for lat, long in zip(list_of_lat, list_of_long):
    list_of_coordinates.append((lat,long))

len(list_of_coordinates)

mrt_lat = mrt_location['latitude']
mrt_long = mrt_location['longitude']
list_of_mrt_coordinates = []

for lat, long in zip(mrt_lat, mrt_long):
    list_of_mrt_coordinates.append((lat, long))
    
len(list_of_mrt_coordinates)

from geopy.distance import geodesic

test_coordinate_list = list_of_coordinates[0]
list_of_dist = []
min_dist = []

for origin in list_of_coordinates:
    for destination in range(0, len(list_of_mrt_coordinates)):
        list_of_dist.append(geodesic(origin,list_of_mrt_coordinates[destination]).meters)
    smallest = (min(list_of_dist))
    min_dist.append(smallest)
    list_of_dist.clear()
    
df_coordinates['dist_to_mrt'] = min_dist

combined = df_coordinates.merge(df_hdb_price, on="address", how='outer') 

combined = combined.dropna()
combined.isna().sum()
