import geopandas as gpd
import pandas as pd
import numpy as np
import libpysal
import libpysal as lp
from libpysal.weights import Queen
import seaborn as sns
import matplotlib.pyplot as plt

#Read shapefile using Geopandas
shapefile = 'ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp'
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry', 'CONTINENT']]
df = pd.DataFrame(gdf)

#read data on life expectancy
df_happiness = pd.read_csv('happiness-cantril-ladder.csv')

#create list with just the countries in africa
list_africa = []
for index, row in df.iterrows():
    if row['CONTINENT'] == 'Africa':
        list_africa.append(row)

#create dataframe
df_africa = pd.DataFrame(list_africa)
gf_africa = gpd.GeoDataFrame(df_africa)

#Rename columns.
gf_africa.columns = ['country', 'country_code', 'geometry', 'continent']
#create list of African countries
african_countries_list = gf_africa['country_code'].tolist()
#create dictionary holding life expectancy values of African countries
african_satisfaction_dict = dict.fromkeys(african_countries_list, None)

count = 0
#filter out non-African countries and entries that aren't from 2016 from dataframe
for index, row in df_happiness.iterrows():
    if row['Code'] in african_countries_list:
        if row['Year'] == 2017:
            count += 1
            african_satisfaction_dict[row['Code']] = row['Life satisfaction in ' \
                                                     'Cantril Ladder (World Happiness ' \
                                                     'Report 2019)']

#print('Number of countries found: ' + str(count))
#for key, value in african_satisfaction_dict.items():
    #if value == None:
        #print(key)


#create additional columns for analysis
df_africa['happiness'] = None
df_africa['color_happiness'] = None
df_africa['location'] = None
df_africa['happiness_stand'] = None
df_africa['spatial_lag_stand'] = None

#add life expectancy values from dict to dataframe
for index, row in df_africa.iterrows():
    df_africa.at[index, 'happiness'] = african_satisfaction_dict[row['country_code']]

max_happiness = df_africa['happiness'].max()
min_happiness = df_africa['happiness'].min()

#set the colour of a node based on its relative life expectancy
for index, row in df_africa.iterrows():
    if row['happiness'] is not None:
        df_africa.at[index, 'color_happiness'] = (row['happiness'] / max_happiness)
    else:
        df_africa.at[index, 'color_happiness'] = 0

#define North and West African countries by country_code
north_african_countries = ['DZA', 'EGY', 'LBY', 'SDN', 'TUN']
west_african_countries = ['BEN', 'BFA', 'CPV', 'CIV', 'GMB', 'GHA', 'GNB',
                         'LBR', 'MLI', 'MRT', 'NER', 'NGA', 'SEN', 'SLE', 'TGO']

for index, row in df_africa.iterrows():
    if row['country_code'] in north_african_countries:
        df_africa.at[index, 'location'] = 'N'
    if row['country_code'] in west_african_countries:
        df_africa.at[index, 'location'] = 'W'

gf_africa = gpd.GeoDataFrame(df_africa)


'''
#Rename columns.
gf_africa.columns = ['country', 'country_code', 'geometry', 'continent',
                     'life_exp', 'color', 'location', 'life_exp_stand',
                     'spatial_lag_stand']

#change life_exp column values to numeric
df_africa['life_exp'] = pd.to_numeric(df_africa['life_exp'])
df_africa['life_exp_stand'] = pd.to_numeric(df_africa['life_exp_stand'])
df_africa['spatial_lag_stand'] = pd.to_numeric(df_africa['spatial_lag_stand'])

y = df_africa['life_exp']
#standard deviation of life expectancy
y_std = np.std(df_africa['life_exp'])
#mean value of life expectancy
y_mean = np.mean(df_africa['life_exp'])
#create column with standardized values of life expectancy
for index, row in df_africa.iterrows():
    df_africa.at[index, 'life_exp_stand'] = (row['life_exp'] - y_mean) / y_std

#define queens weight matrix
w = Queen.from_dataframe(gf_africa)
w.transform = 'r'

#calculate the spatial lag
yl = libpysal.weights.lag_spatial(w, y)
#add spatial lag column to df
df_africa['spatial_lag'] = yl
#standard deviation of yl
yl_std = np.std(df_africa['spatial_lag'])
#mean value of yl
yl_mean = np.mean(df_africa['spatial_lag'])
#create column with standardized values of spatial lag
for index, row in df_africa.iterrows():
    df_africa.at[index, 'spatial_lag_stand'] = (row['spatial_lag'] - yl_mean) / yl_std

#drop African islands with no Queen's neighbour
df_africa.drop(df_africa.tail(4).index, inplace=True)

#label countries as being either North or West African
df_africa_N = df_africa[df_africa['location'] == 'N']
df_africa_W = df_africa[df_africa['location'] == 'W']
df_africa_NW = pd.concat([df_africa_N, df_africa_W])

sns.scatterplot(x='life_exp_stand', y='spatial_lag_stand', data=df_africa_NW, hue='location')

#sns.regplot(x='life_exp_stand', y='spatial_lag_stand', data=df_africa_NW)

#g = sns.jointplot()
#sns.regplot(x="life_exp_stand",  y="spatial_lag_stand", ax=g.ax_joint, scatter=False, data=df_africa_NW)
#sns.scatterplot(x='life_exp_stand', y='spatial_lag_stand', data=df_africa_NW, hue='location', ax=g.ax_joint)

# Add vertical and horizontal lines
plt.axvline(0, c='k', alpha=0.5)
plt.axhline(0, c='k', alpha=0.5)
#set plot title
plt.title('Moran plot of life expectancy in North and West African countries')
# Set x-axis label
plt.xlabel('Standardized life expectancy (std dev)')
# Set y-axis label
plt.ylabel('Standardized spatial lag (std dev)')
plt.legend(loc='lower right')

#define node labels
def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))

#add node labels to plot
label_point(df_africa_NW.life_exp_stand, df_africa_NW.spatial_lag_stand, df_africa_NW.country, plt.gca())

#display plot
plt.show()

#gf_africa.plot(column='color', cmap='Wistia')
#plt.show()



#print connected countries of specific country
'''

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