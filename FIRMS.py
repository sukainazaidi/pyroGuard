#NASA FIRMS API for heatmap

import requests
import folium
import csv
from io import StringIO
import webbrowser
import sys
import pandas as pd
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt


url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/949529f31f55f4b6ce5b67f2e06e1057/LANDSAT_NRT/world/1/"
#url = 'https://firms.modaps.eosdis.nasa.gov/api/country/csv/949529f31f55f4b6ce5b67f2e06e1057/VIIRS_SNPP_NRT/USA/1'

def heatmap():
    print("Getting NASA info")

    # Make API request
    response = requests.get(url)

    if response.status_code == 200:
        csv_data = response.text

        #csv reader
        df = pd.read_csv(StringIO(csv_data))

        # Basic data analysis
        print("Basic Data Analysis:")
        print(df.describe())


        # Plot a histogram of confidence levels
        plt.figure(figsize=(8, 6))
        df['confidence'].hist(bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribution of Confidence Levels')
        plt.xlabel('Confidence Level')
        plt.ylabel('Frequency')
        plt.show()
        
        # creating map with active fires marked
        m = folium.Map(location = [34.0522, -118.2437], zoom_start = 5)

        for row in df.iterrows():
            latitude = row[1]['latitude']
            longitude = row[1]['longitude']
            
            #markers for fire hotspots
            folium.Circle(
                location = [latitude, longitude],
                radius = 1000,
                color = 'red',
                fill = True,
                fill_color = 'red',
                fill_opacity = 0.5,
            ).add_to(m)

        # Save the map as an HTML file
        m.save('wildfire_map.html')

        print('Map is created!')

        webbrowser.open('wildfire_map.html')

    else:
        print(f"Failed to retrieve data from the NASA API. Status code: {response.status_code}")


heatmap()
