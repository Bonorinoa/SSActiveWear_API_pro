# scripts/sync_data.py
import requests
import pandas as pd
import sys
import os

# This allows the script to import modules from the parent directory (the 'app' package)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, settings

# --- CONFIGURATION ---
URL_STYLES = "https://api.ssactivewear.com/v2/styles/"
URL_PRODUCTS = "https://api.ssactivewear.com/v2/products/"

def fetch_and_load_data():
    """Fetches data from SS Activewear and loads it into the PostgreSQL database."""
    print("🚀 Starting data sync...")

    auth = (settings.ss_username, settings.ss_password)

    try:
        # 1. Fetch Styles Data
        print("Fetching styles...")
        styles_response = requests.get(URL_STYLES, auth=auth)
        styles_response.raise_for_status()
        styles_df = pd.DataFrame(styles_response.json())
        # Keep only the columns we need for the merge
        styles_df = styles_df[['styleID', 'title', 'baseCategory', 'description', 'sustainableStyle']]
        print(f"✅ Found {len(styles_df)} styles.")

        # 2. Fetch Products Data
        print("Fetching products... (This may take a few minutes)")
        products_response = requests.get(URL_PRODUCTS, auth=auth)
        products_response.raise_for_status()
        products_df = pd.DataFrame(products_response.json())
        # Keep only the columns that match our database model
        products_df = products_df[['sku', 'styleID', 'brandName', 'colorName', 'sizeName', 'piecePrice', 'qty', 'colorFrontImage', 'colorBackImage', 'colorSwatchImage', 'colorSwatchTextColor']]
        print(f"✅ Found {len(products_df)} products.")

        # 3. Combine and Prepare Data
        print("Combining and preparing data...")
        # Merge product data with style data
        combined_df = pd.merge(products_df, styles_df, on='styleID', how='left')
        # Handle potential missing data for boolean field
        combined_df['sustainableStyle'] = combined_df['sustainableStyle'].fillna(False)
        print("✅ Data combined.")
        
        # 4. Load to Database
        print("⏳ Loading data into PostgreSQL... (This will take several minutes)")
        
        # Use pandas.to_sql to load the DataFrame into the 'products' table.
        # 'if_exists='replace'' will drop the table first and then create a new one.
        # 'chunksize' processes the data in batches to manage memory usage.
        combined_df.to_sql(
            'products', 
            engine, 
            if_exists='replace', 
            index=False, 
            chunksize=10000 
        )
        
        print("✅ Data sync complete! Your database is ready.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data from API: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_and_load_data()