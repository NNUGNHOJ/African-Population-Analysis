import geopandas as gpd
import pandas as pd
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

#print(df_exp_edu.columns)
#print(df_exp_edu.head(5))

african_countries_edu_spending_dict = dict.fromkeys(african_countries_list, {})

for index, row in df_exp_edu.iterrows():
    if row['Entity'] in african_countries_list:
        african_countries_edu_spending_dict[row['Entity']].update({row['Year']:
                                                                       row['Government expenditure on education, '
                                                                       'total (% of government expenditure)']})

#african_countries_edu_spending_dict = collections.OrderedDict(sorted(african_countries_edu_spending_dict.items()))
#print(african_countries_edu_spending_dict)

df_africa.insert(2, "expen_edu", [{},{},{},{},{},{},{},{},{},
                                  {},{},{},{},{},{},{},{},{},
                                  {},{},{},{},{},{},{},{},{},
                                  {},{},{},{},{},{},{},{},{},
                                  {},{},{},{},{},{},{},{},{},
                                  {},{},{},{},{},{},{},{},{},], True)

for index, row in df_africa.iterrows():
    country_name = row['country']
    if country_name in african_countries_list:
        row['expen_edu'] = african_countries_edu_spending_dict[row['country']]



print(df_africa[['expen_edu']])
#gf_africa.plot()
#plt.show()