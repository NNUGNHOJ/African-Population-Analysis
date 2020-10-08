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

#read data on education
df_exp_edu = pd.read_csv('government-expenditure-education.csv')

african_countries_edu_spending_dict = dict.fromkeys(african_countries_list, 0)

for index, row in df_exp_edu.iterrows():
    if row['Entity'] in african_countries_list:
        if row['Year'] == 2014:
            african_countries_edu_spending_dict[row['Entity']] = row['Government expenditure on education, ' 
                                                                     'total (% of government expenditure)']

df_africa['edu_spending'] = 0
df_africa['color'] = 0

for index, row in df_africa.iterrows():
    df_africa.at[index, 'edu_spending'] = african_countries_edu_spending_dict[row['country']]

print(df_africa.head(10))

gf_africa = gpd.GeoDataFrame(df_africa)
#Rename columns.
gf_africa.columns = ['country', 'country_code', 'geometry', 'continent', 'edu_spending', 'color']

gf_africa['color_rgba'] = gf_africa.apply(
    lambda row: to_rgba(row['color'], alpha=row['edu_spending']), axis=1)
gf_africa.plot(color=gf_africa['color_rgba'])

'''
#gf_africa.plot()
#plt.show()

gdf['color_rgba'] = gdf.apply(
    lambda row: to_rgba(row['color'], alpha=row['margin']), axis=1)
gdf.plot(color=gdf['color_rgba'])

'''