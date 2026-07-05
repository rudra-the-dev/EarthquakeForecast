import requests
import pandas as pd
import os

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def fetch_earthquakes(start="2015-01-01", end="2026-01-01", min_magnitude=2.0):
    params = {
        "format": "geojson",
        "starttime": start,
        "endtime": end,
        "minmagnitude": min_magnitude
    }

    print("Downloading earthquake data...")

    response = requests.get(URL, params=params)
    data = response.json()

    features = data["features"]

    rows = []
    for f in features:
        props = f["properties"]
        coords = f["geometry"]["coordinates"]

        rows.append({
            "time": props["time"],
            "magnitude": props["mag"],
            "place": props["place"],
            "longitude": coords[0],
            "latitude": coords[1],
            "depth": coords[2],
        })

    df = pd.DataFrame(rows)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/earthquakes_raw.csv", index=False)

    print(f"Saved {len(df)} records to data/earthquakes_raw.csv")

if __name__ == "__main__":
    fetch_earthquakes()