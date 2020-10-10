import geopandas as gpd
import pandas as pd
import seaborn as sns
import pysal as ps
from matplotlib.colors import to_rgba
from matplotlib import cm
import collections
import matplotlib
import matplotlib.pyplot as plt

#Read shapefile using Geopandas
shapefile = 'ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp'
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry', 'CONTINENT']]
df = pd.DataFrame(gdf)


'''
#read data on life expectancy
df_life_exp = pd.read_csv('life_exp.csv')

#create df with just the countries in africa
list_africa = []
for index, row in df.iterrows():
    if row['CONTINENT'] == 'Africa':
        list_africa.append(row)

df_africa = pd.DataFrame(list_africa)
gf_africa = gpd.GeoDataFrame(df_africa)

#Rename columns.
gf_africa.columns = ['country', 'country_code', 'geometry', 'continent']
#create list of African countries
african_countries_list = gf_africa['country_code'].tolist()

african_life_exp_dict = dict.fromkeys(african_countries_list, None)

for index, row in df_life_exp.iterrows():
    if row['Code'] in african_countries_list:
        if row['Year'] == 2016:
            african_life_exp_dict[row['Code']] = row['Life expectancy at birth, total (years)']


df_africa['life_exp'] = None
df_africa['color'] = None
df_africa['location'] = None

for index, row in df_africa.iterrows():
    df_africa.at[index, 'life_exp'] = african_life_exp_dict[row['country_code']]

max_life_exp = df_africa['life_exp'].max()
min_life_exp = df_africa['life_exp'].min()

for index, row in df_africa.iterrows():
    if row['life_exp'] is not None:
        df_africa.at[index, 'color'] = (row['life_exp'] / max_life_exp)
    else:
        df_africa.at[index, 'color'] = 0
        
north_african_countries = ['DZA', 'EGY', 'LBY', 'SDN', 'TUN']
west_african_countries = ['BEN', 'BFA', 'CPV', 'CIV', 'GMB', 'GHA', 'GNB',
                         'LBR', 'MLI', 'MRT', 'NER', 'NGA', 'SEN', 'SLE', 'TGO']

for index, row in df_africa.iterrows():
    if row['country_code'] in north_african_countries:
        df_africa.at[index, 'location'] = 'N'
    if row['country_code'] in west_african_countries:
        df_africa.at[index, 'location'] = 'W'

gf_africa = gpd.GeoDataFrame(df_africa)

#Rename columns.
gf_africa.columns = ['country', 'country_code', 'geometry', 'continent', 'life_exp', 'color', 'location']

#gf_africa.plot(column='color', cmap='Wistia')
#plt.show()

#turn geodataframe into shapefile
#gf_africa.to_file("result2.shp")

'''

#Contiguity weights matrix using queen contiguity
w_queen = ps.queen_from_shapefile(shapefile, idVariable='ADM0_A3')

weight_between_NAM_and_ZAF = w_queen['NAM']['ZAF']
all_neighbours_of_NAM = w_queen['NAM']

#print connects countries of specific country
'''
gdf = gdf.set_index('ADM0_A3')
# Setup figure
f, ax = plt.subplots(1, figsize=(6, 6))
# Plot base layer of polygons
gdf.plot(ax=ax, facecolor='k', linewidth=0.1)

# NOTE we pass both the area code and the column name
#      (`geometry`) within brackets!!!
focus = gdf.loc[['NAM'], ['geometry']]
# Plot focal polygon
focus.plot(facecolor='red', alpha=1, linewidth=0, ax=ax)
# Plot neighbors
neis = gdf.loc[w_queen['NAM'], :]
neis.plot(ax=ax, facecolor='orange', linewidth=0)
# Title
f.suptitle("Queen neighbors of `NAM`")
# Style and display on screen
plt.show()
'''


#block weights
#lookup = gf_africa['location']
#w_block = ps.block_weights(gf_africa['location'])
