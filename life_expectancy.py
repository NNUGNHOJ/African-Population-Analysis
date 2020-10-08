import geopandas as gpd
import pandas as pd
from matplotlib.colors import to_rgba
import collections
import matplotlib
import matplotlib.pyplot as plt

#Read shapefile using Geopandas
shapefile = 'ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp'
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry', 'CONTINENT']]
df = pd.DataFrame(gdf)

#read data on life expectancy
df_life_exp = pd.read_csv('life_exp.csv')

print(df_life_exp.columns)

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
african_countries_list = gf_africa['country'].tolist()

african_life_exp_dict = dict.fromkeys(african_countries_list, None)

for index, row in df_life_exp.iterrows():
    if row['Entity'] in african_countries_list:
        if row['Year'] == 2016:
            african_life_exp_dict[row['Entity']] = row['Life expectancy at birth, total (years)']

df_africa['life_exp'] = None
df_africa['color'] = None

for index, row in df_africa.iterrows():
    df_africa.at[index, 'life_exp'] = african_life_exp_dict[row['country']]

max_life_exp = df_africa['life_exp'].max()
min_life_exp = df_africa['life_exp'].min()

for index, row in df_africa.iterrows():
    if row['life_exp'] is not None:
        df_africa.at[index, 'color'] = (row['life_exp'] / max_life_exp)

print(df_africa.head(10))

gf_africa = gpd.GeoDataFrame(df_africa)
#Rename columns.
gf_africa.columns = ['country', 'country_code', 'geometry', 'continent', 'life_exp', 'color']


gf_africa['color_rgba'] = gf_africa.apply(
    lambda row: to_rgba(row['color'], alpha=row['life_exp']), axis=1)
gf_africa.plot(color=gf_africa['color_rgba'])

'''

#gf_africa.plot()
#plt.show()

gdf['color_rgba'] = gdf.apply(
    lambda row: to_rgba(row['color'], alpha=row['margin']), axis=1)
gdf.plot(color=gdf['color_rgba'])

'''