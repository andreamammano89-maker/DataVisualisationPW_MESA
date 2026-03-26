"""
download_airbnb_data.py

Downloads the latest Airbnb listings data from Inside Airbnb for:
  - Rome, Italy
  - Copenhagen, Denmark

Saves each dataset to:
  data/rome/listings.csv
  data/copenhagen/listings.csv

Source: http://insideairbnb.com/get-the-data/
Note: URLs point to the most recent quarterly snapshot at time of writing.
      If data is unavailable, check the Inside Airbnb website for updated URLs.
"""

import os
import urllib.request

# ---------------------------------------------------------------------------
# Dataset URLs — Inside Airbnb (listings.csv.gz, decompressed automatically)
# ---------------------------------------------------------------------------
DATASETS = {
    "rome": {
        # Latest scrape: 14 September 2025
        "url": "https://data.insideairbnb.com/italy/lazio/rome/2025-09-14/data/listings.csv.gz",
        "dir": "data/rome",
        "filename": "listings.csv",
    },
    "copenhagen": {
        # Latest scrape: 29 September 2025
        "url": "https://data.insideairbnb.com/denmark/hovedstaden/copenhagen/2025-09-29/data/listings.csv.gz",
        "dir": "data/copenhagen",
        "filename": "listings.csv",
    },
}

# ---------------------------------------------------------------------------
# Download helper
# ---------------------------------------------------------------------------

def download_and_extract(city: str, config: dict) -> None:
    """Download a gzipped CSV from Inside Airbnb and save as plain CSV."""
    import gzip
    import shutil

    out_dir = config["dir"]
    os.makedirs(out_dir, exist_ok=True)

    gz_path = os.path.join(out_dir, "listings.csv.gz")
    csv_path = os.path.join(out_dir, config["filename"])

    # Skip if already downloaded
    if os.path.exists(csv_path):
        print(f"[{city}] Already exists — skipping download.")
        return

    print(f"[{city}] Downloading from {config['url']} ...")
    urllib.request.urlretrieve(config["url"], gz_path)

    print(f"[{city}] Extracting to {csv_path} ...")
    with gzip.open(gz_path, "rb") as f_in, open(csv_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    os.remove(gz_path)
    print(f"[{city}] Done. Saved to {csv_path}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    os.chdir(base_dir)

    for city, config in DATASETS.items():
        download_and_extract(city, config)

    print("All datasets ready.")
