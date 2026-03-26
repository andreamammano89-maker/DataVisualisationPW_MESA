import urllib.request
import re
import os

url = "https://insideairbnb.com/get-the-data/"
print("Fetching Inside Airbnb data page...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    # Look for links containing milan
    # The format is typically: https://data.insideairbnb.com/italy/lombardy/milan/2024-03-21/data/listings.csv.gz
    # or visualisations/listings.csv
    links = re.findall(r'href="(https://data\.insideairbnb\.com/[^"]*milan/[^"]*)"', html)
    
    unique_links = sorted(list(set(links)))
    
    os.makedirs('data', exist_ok=True)
    
    listings_csv_links = [l for l in unique_links if l.endswith('visualisations/listings.csv') or l.endswith('data/listings.csv.gz')]
    
    if listings_csv_links:
        print("Found links for Milan:")
        for l in listings_csv_links:
            print(l)
        
        # We want the most recent 'visualisations/listings.csv' and 'visualisations/neighbourhoods.csv'
        latest_date = sorted(list(set(re.findall(r'/milan/([^/]+)/', html))))[-1]
        print(f"Latest date found for Milan: {latest_date}")
        
        target_listing = f"https://data.insideairbnb.com/italy/lombardy/milan/{latest_date}/visualisations/listings.csv"
        target_neighbourhoods = f"https://data.insideairbnb.com/italy/lombardy/milan/{latest_date}/visualisations/neighbourhoods.csv"
        target_geojson = f"https://data.insideairbnb.com/italy/lombardy/milan/{latest_date}/visualisations/neighbourhoods.geojson"
        
        print(f"Downloading {target_listing} to data/listings.csv ...")
        urllib.request.urlretrieve(target_listing, "data/listings.csv")
        
        print(f"Downloading {target_neighbourhoods} to data/neighbourhoods.csv ...")
        urllib.request.urlretrieve(target_neighbourhoods, "data/neighbourhoods.csv")
        
        print(f"Downloading {target_geojson} to data/neighbourhoods.geojson ...")
        urllib.request.urlretrieve(target_geojson, "data/neighbourhoods.geojson")
        
        print("Download complete!")
    else:
        print("Could not find expected links for Milan in the page source.")
        
except Exception as e:
    print(f"Error: {e}")
