import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

query_string='https://data.gov.sg/api/action/datastore_search?resource_id=42ff9cfe-abe5-4b54-beda-c88f9bb438ee&limit=101994'
resp = requests.get(query_string)

#Convert JSON into Python Object 
data = json.loads(resp.content)

# Checking the length of dataframe
len(data['result']['records'])

# Store our dictionart records into hdb_price_dict_records
hdb_price_dict_records = data['result']['records']

# Next we need to feed our JSON data into dataframe. 
# We will access the 'records' key:value pairs of the python dictionary. 
# We will then map the list into a dataframe.
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
df_hdb_price.shape

# Now, the next part gets a little tricky. We need to find the nearest MRT station the HDB unit is located in using their geo-location coordinates (Latitude, Longitude). We will use another API to achieve this - the OneMap API.

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


# In[10]:


list_of_shopping_mall = [
    '100 AM',
    '313@Somerset',
    'Aperia',
    'Balestier Hill Shopping Centre',
    'Bugis Cube',
    'Bugis Junction',
    'Bugis+',
    'Capitol Piazza',
    'Cathay Cineleisure Orchard',
    'City Gate',
    'City Square Mall',
    'CityLink Mall',
    'Clarke Quay Central',
    'Duo',
    'Far East Plaza',
    'Funan',
    'Great World City',
    'HDB Hub',
    'Holland Village Shopping Mall',
    'ION Orchard',
    'Junction 8',
    'Knightsbridge[1]',
    'Liang Court',
    'Liat Towers',
    'Lucky Plaza',
    'Marina Bay Financial Centre Tower 3',
    'Marina Bay Link Mall',
    'Marina Bay Sands',
    'Marina One',
    'Marina Square',
    'Midpoint Orchard',
    'Millenia Walk',
    'Mustafa Shopping Centre',
    'Ngee Ann City',
    'Orchard Central',
    'Orchard Gateway',
    'Orchard Plaza',
    'Orchard Shopping Centre',
    'Palais Renaissance',
    'Peoples Park Centre',
    'Peoples Park Complex',
    'Plaza Singapura',
    'PoMo',
    'Raffles City',
    'Scotts Square',
    'Serangoon Plaza',
    'Shaw House and Centre',
    'Sim Lim Square',
    'Singapore Shopping Centre',
    'Square 2',
    'Suntec City',
    'Tanglin Mall',
    'Tangs',
    'Tanjong Pagar Centre',
    'Tekka Centre',
    'The Centrepoint',
    'The Paragon',
    'The Poiz [2]',
    'The Shoppes at Marina Bay Sands',
    'The South Beach',
    'Thomson Plaza',
    'United Square, The Kids Learning Mall',
    'Velocity',
    'Wheelock Place',
    'Wisma Atria',
    'Zhongshan Mall',
    '112 Katong',
    'Bedok Mall',
    'Bedok Point',
    'Century Square',
    'Changi Airport',
    'Changi City Point',
    'City Plaza',
    'Djitsun Mall Bedok',
    'Downtown East',
    'East Village',
    'Eastpoint Mall',
    'Elias Mall',
    'Kallang Wave Mall',
    'Katong Square',
    'Katong V',
    'KINEX (formerly One KM Mall)',
    'Leisure Park Kallang',
    'Loyang Point',
    'Our Tampines Hub',
    'Parkway Parade',
    'Paya Lebar Square',
    'PLQ Mall',
    'Singapore Post Centre',
    'Tampines 1',
    'Tampines Mall',
    'The Flow',
    'White Sands',
    '888 Plaza',
    'Admiralty Place',
    'AMK Hub',
    'Beauty World Centre',
    'Beauty World Plaza',
    'Broadway Plaza',
    'Buangkok Square',
    'Bukit Panjang Plaza',
    'Bukit Timah Plaza',
    'Causeway Point',
    'Compass One',
    'Djitsun Mall',
    'Fajar Shopping Centre',
    'Greenridge Shopping Centre',
    'Greenwich V',
    'Heartland Mall',
    'Hillion Mall',
    'HillV2',
    'Hougang 1',
    'Hougang Green Shopping Mall',
    'Hougang Mall',
    'Jubilee Square',
    'Junction 10',
    'Junction 9',
    'Keat Hong Shopping Centre',
    'KKH The Retail Mall',
    'Limbang Shopping Centre',
    'Lot One',
    'Marsiling Mall',
    'myVillage @ Serangoon',
    'NEX',
    'North East',
    'North West',
    'Northpoint City',
    'Oasis Terraces',
    'Punggol Plaza',
    'Rail Mall',
    'Rivervale Mall',
    'Rivervale Plaza',
    'Sembawang Shopping Centre',
    'Sun Plaza',
    'Sunshine Place',
    'Teck Whye Shopping Centre',
    'The Midtown',
    'The Seletar Mall',
    'Upper Serangoon Shopping Centre',
    'Waterway Point',
    'West Mall',
    'Wisteria Mall',
    'Woodlands Mart',
    'Yew Tee Point',
    'Yew Tee Shopping Centre',
    'Yew Tee Square',
    'Alexandra Retail Centre',
    'HarbourFront Centre',
    'VivoCity',
    '321 Clementi',
    'Alexandra Central',
    'Anchorpoint',
    'Big Box',
    'Boon Lay Shopping Centre',
    'Fairprice Hub',
    'Gek Poh Shopping Centre',
    'Grantral Mall',
    'IMM',
    'JCube',
    'Jem',
    'Jurong Point',
    'OD Mall',
    'Pioneer Mall',
    'Queensway Shopping Centre',
    'Rochester Mall',
    'Taman Jurong Shopping Centre',
    'The Clementi Mall',
    'The Star Vista',
    'Tiong Bahru Plaza',
    'West Coast Plaza',
    'Westgate Mall',
]


# We will use the OneMap API to obtain the (lat, long) coordinates of each MRT station.
# Obtaining MRT coordinates in Singapore
mrt_lat = []
mrt_long = []

for i in range(0, len(list_of_mrt)):
    query_address = list_of_mrt[i]
    query_string = 'https://developers.onemap.sg/commonapi/search?searchVal='+str(query_address)+'&returnGeom=Y&getAddrDetails=Y'
    resp = requests.get(query_string)

    data_mrt=json.loads(resp.content)
    
    if data_mrt['found'] != 0:
        mrt_lat.append(data_mrt["results"][0]["LATITUDE"])
        mrt_long.append(data_mrt["results"][0]["LONGITUDE"])

        print (str(query_address)+",Lat: "+data_mrt['results'][0]['LATITUDE'] +" Long: "+data_mrt['results'][0]['LONGITUDE'])

    else:
        mrt_lat.append('NotFound')
        mrt_lat.append('NotFound')
        print ("No Results")

# Store this information in a dataframe
mrt_location = pd.DataFrame({
    'MRT': list_of_mrt,
    'Latitude': mrt_lat,
    'Longitude': mrt_long
})

mrt_location.head()

# Obtaining Mall Coordinates in Singapore
mall_name = []
mall_roadname = []
mall_lat = []
mall_long = []

for i in range(0, len(list_of_shopping_mall)):
    query_address = list_of_shopping_mall[i]
    query_string = 'https://developers.onemap.sg/commonapi/search?searchVal='+str(query_address)+'&returnGeom=Y&getAddrDetails=Y'
    resp = requests.get(query_string)
    data_mall=json.loads(resp.content)
    
    if data_mall['found'] != 0:
        mall_name.append(query_address)
        mall_roadname.append(data_mall["results"][0]["ROAD_NAME"])
        mall_lat.append(data_mall["results"][0]["LATITUDE"])
        mall_long.append(data_mall["results"][0]["LONGITUDE"])

        print (str(query_address)+" ,Lat: "+data_mall['results'][0]['LATITUDE'] +" Long: "+data_mall['results'][0]['LONGITUDE'])

    else:
        print ("No Results")

# Store this information in a dataframe
mall_location = pd.DataFrame({
    'Mall': mall_name,
    'RoadName': mall_roadname,
    'Latitude': mall_lat,
    'Longitude': mall_long
})

# Now - let's find grab the geolocation of each unit that was transacated using the same method. But hang on - that's a large dataset.. we can make it a bit more efficient. We know that there will be multiple units that will be transacted in the same HDB Apartment block. We can de-dup our dataframe and obtion the only unique addresses in our dataframe. 
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
    #formulate query string  
    query_address = address_list[row]
    query_string='https://developers.onemap.sg/commonapi/search?searchVal='+str(query_address)+'&returnGeom=Y&getAddrDetails=Y'
    resp = requests.get(query_string)          

    #Convert JSON into Python Object 
    data_geo_location=json.loads(resp.content)
    if data_geo_location['found'] != 0:
        latitude.append(data_geo_location['results'][0]['LATITUDE'])
        longitude.append(data_geo_location['results'][0]['LONGITUDE'])
        blk_no.append(data_geo_location['results'][0]['BLK_NO'])
        road_name.append(data_geo_location['results'][0]['ROAD_NAME'])
        postal_code.append(data_geo_location['results'][0]['POSTAL'])
        address.append(query_address)
        print (str(query_address) + " ,Lat: " + data_geo_location['results'][0]['LATITUDE'] + " Long: " + data_geo_location['results'][0]['LONGITUDE'])
    else:
        print ("No Results")

# Fit into a dataframe
df_coordinates = pd.DataFrame({
    'latitude': latitude,
    'longitude': longitude,
    'blk_no': blk_no,
    'road_name': road_name,
    'postal_code': postal_code,
    'address': address
})

df_coordinates.shape

# Awesome! Now we have both the lat and long of our dataset. 
list_of_lat = df_coordinates['latitude']
list_of_long = df_coordinates['longitude']

# List if coordinates of all unique addresses in our dataset
list_of_coordinates = []
for lat, long in zip(list_of_lat, list_of_long):
    list_of_coordinates.append((lat,long))

len(list_of_coordinates)

# List of MRT Coordinates in Singapore
mrt_lat = mrt_location['Latitude']
mrt_long = mrt_location['Longitude']

list_of_mrt_coordinates = []

for lat, long in zip(mrt_lat, mrt_long):
    list_of_mrt_coordinates.append((lat, long))
    
len(list_of_mrt_coordinates)

# List of Shopping Mall Coordinates in Singapore
mall_lat = mall_location['Latitude']
mall_long = mall_location['Longitude']

list_of_mall_coordinates = []

for lat, long in zip(mall_lat, mall_long):
    list_of_mall_coordinates.append((lat, long))
    
len(list_of_mall_coordinates)

# Distance to nearest MRT
from geopy.distance import geodesic

list_of_dist_mrt = []
min_dist_mrt = []

for origin in list_of_coordinates:
    for destination in range(0, len(list_of_mrt_coordinates)):
        list_of_dist_mrt.append(geodesic(origin,list_of_mrt_coordinates[destination]).meters)
    shortest = (min(list_of_dist_mrt))
    min_dist_mrt.append(shortest)
    list_of_dist_mrt.clear()

# Distance from nearest mall
list_of_dist_mall = []
min_dist_mall = []

for origin in list_of_coordinates:
    for destination in range(0, len(list_of_mall_coordinates)):
        list_of_dist_mall.append(geodesic(origin,list_of_mall_coordinates[destination]).meters)
    shortest = (min(list_of_dist_mall))
    print(shortest)
    min_dist_mall.append(shortest)
    list_of_dist_mall.clear()
    
# Distance from CDB
cbd_dist = []

for origin in list_of_coordinates:
    cbd_dist.append(geodesic(origin,(1.2830, 103.8513)).meters)

# Putting it all together
df_coordinates['min_dist_mrt'] = min_dist_mrt
df_coordinates['min_dist_mall'] = min_dist_mall
df_coordinates['cbd_dist'] = cbd_dist

df_coordinates.head()

combined = df_coordinates.merge(df_hdb_price, on="address", how='outer')

# Data Cleaning and Hygiene
combined['resale_price'] = combined['resale_price'].astype('float')
combined['floor_area_sqm'] = combined['floor_area_sqm'].astype('float')
combined['lease_commence_date'] = combined['lease_commence_date'].astype('int64')
combined['lease_remain_years'] = 2019 - combined['lease_commence_date']
combined.columns

combined.dropna(inplace=True)

combined['price_per_sqm'] = combined['resale_price'].div(combined['floor_area_sqm'])

# Plotting Bit-Rent Scatterplot
fig, ax1 = plt.subplots(1,1, figsize=(20,12))
g = sns.scatterplot(x=combined['cbd_dist'],y=combined['price_per_sqm'], hue=combined['flat_type'], ax=ax1) 

box = g.get_position()
g.set_position([box.x0, box.y0, box.width * 0.85, box.height]) # resize position

g.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), ncol=1)

plt.show()

# Let's examine the correlation between our features
df_numerical_cols = combined[['min_dist_mrt', 'min_dist_mall', 'cbd_dist','floor_area_sqm', 'lease_remain_years', 'resale_price', 'price_per_sqm']]

df_numerical_cols.describe().round(0)

df_numerical_cols.dropna(inplace=True)

df_numerical_cols.isna().sum()


corrMatrix = df_numerical_cols.corr()
sns.heatmap(corrMatrix, 
        xticklabels=corrMatrix.columns,
        yticklabels=corrMatrix.columns,
        cmap='coolwarm',
        annot=True)

# Separate our numerical and categorical variables
cat_features = ['town', 'flat_type', 'storey_range']
num_features = ['min_dist_mrt', 'min_dist_mall', 'cbd_dist','floor_area_sqm', 'lease_remain_years', 'resale_price', 'price_per_sqm']
target = ['resale_price']

df_reg = combined[['town', 'flat_type', 'storey_range', 'min_dist_mrt', 'min_dist_mall', 'cbd_dist','floor_area_sqm', 'lease_remain_years', 'resale_price', 'price_per_sqm']]

df_reg['flat_type'].value_counts()

# Mapping ordinal categories to their respective values
flat_type_map = {
    'EXECUTIVE': 7,
    'MULTI-GENERATION': 6,
    '5 ROOM': 5,
    '4 ROOM': 4,
    '3 ROOM': 3,
    '2 ROOM': 2,
    '1 ROOM': 1
}

df_reg['flat_type_mapped'] = df_reg['flat_type'].map(lambda x: flat_type_map[x])

df_reg.head()

df_reg['storey_range'].value_counts()

def split_mean(x):
    split_list = x.split(' TO ')
    mean = (float(split_list[0])+float(split_list[1]))/2
    return mean

df_reg['storey_mean'] = df_reg['storey_range'].apply(lambda x: split_mean(x))

df_reg.head()

# One-Hot Encoding for our categorical variables and drop 1 of our dummy variables
df_reg = pd.get_dummies(data=df_reg, columns=['town'], drop_first=True)

df_reg.columns

# Creating our Linear Regression Model
import statsmodels.api as sm
X = df_reg[['min_dist_mrt', 'min_dist_mall',
       'cbd_dist', 'floor_area_sqm', 'lease_remain_years',
       'flat_type_mapped', 'storey_mean', 'town_BEDOK',
       'town_BISHAN', 'town_BUKIT BATOK', 'town_BUKIT MERAH',
       'town_BUKIT PANJANG', 'town_BUKIT TIMAH', 'town_CENTRAL AREA',
       'town_CHOA CHU KANG', 'town_CLEMENTI', 'town_GEYLANG', 'town_HOUGANG',
       'town_JURONG EAST', 'town_JURONG WEST', 'town_KALLANG/WHAMPOA',
       'town_MARINE PARADE', 'town_PASIR RIS', 'town_PUNGGOL',
       'town_QUEENSTOWN', 'town_SEMBAWANG', 'town_SENGKANG', 'town_SERANGOON',
       'town_TAMPINES', 'town_TOA PAYOH', 'town_WOODLANDS', 'town_YISHUN']] 

y = df_reg["price_per_sqm"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

df_reg['pred_error'] = predictions - df_reg["price_per_sqm"]
df_reg['pred_error'].abs().mean()

df_reg["price_per_sqm"].mean()

# Obtaining our Model Performance Metrics
from sklearn import metrics

print('Mean Absolute Error:', metrics.mean_absolute_error(df_reg["price_per_sqm"], predictions))  
print('Mean Squared Error:', metrics.mean_squared_error(df_reg["price_per_sqm"], predictions))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(df_reg["price_per_sqm"], predictions)))
