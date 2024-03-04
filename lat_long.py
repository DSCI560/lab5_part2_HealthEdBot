import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from icecream import ic

OUTPUT_FILENAME = "lab5_pt2/output.csv"
LIST_OF_COLS = ["API #", "Well Name", "Operator Name", "County", "State", "Latitude", "Longitude"]

def get_lat_long(api_no):
    URL = f"https://www.shalexp.com/search/wells?a1=on&f1=api_no&c1=contains&v1={api_no}&dc=wells.0-1-3-4-5-12-13"
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        tables = pd.read_html(response.text)  # Assuming the target data is in table format
        well_data = tables[0][LIST_OF_COLS]
        return well_data
    except Exception as e:
        print(f"Error fetching data for API #: {api_no}. Error: {e}")
        return pd.DataFrame(columns=LIST_OF_COLS)  # Return an empty DataFrame on error

# Load API numbers
drilling_df = pd.read_csv("Final_Preprocessed_Complete.csv", usecols=["API #"])

# Use ThreadPoolExecutor to parallelize requests
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(get_lat_long, drilling_df["API #"]))

# Combine results into a single DataFrame
final_df = pd.concat(results, ignore_index=True)
ic(final_df)
final_df.to_csv(OUTPUT_FILENAME, index=False)