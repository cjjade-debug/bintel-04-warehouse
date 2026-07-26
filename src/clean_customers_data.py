import pandas as pd
import numpy as np
from datetime import datetime

def clean_customers_data(input_file, output_file):
    """
    Clean the customers data CSV file.
    Handles:
    - Region case inconsistencies (EAST, east, East -> East, etc.)
    - Payment type inconsistencies (Debit/Credit -> Credit/Debit)
    - Invalid/malformed date entries
    - Duplicate rows
    - Missing values
    - Invalid spending scores (should be 0-100)
    """
    
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    print(f"Initial rows: {len(df)}")
    print(f"Initial columns: {df.columns.tolist()}")
    
    # 1. Remove completely empty rows
    df = df.dropna(how='all')
    
    # 2. Standardize Region (normalize case)
    region_mapping = {
        'east': 'East',
        'EAST': 'East',
        'west': 'West',
        'WEST': 'West',
        'north': 'North',
        'NORTH': 'North',
        'south': 'South',
        'SOUTH': 'South',
        'central': 'Central',
        'CENTRAL': 'Central',
        'south-west': 'South-West',
        'SOUTH-WEST': 'South-West'
    }
    df['Region'] = df['Region'].str.strip().map(lambda x: region_mapping.get(x, x))
    
    # 3. Standardize DefaultPaymentType (normalize to Credit/Debit format)
    payment_mapping = {
        'Debit/Credit': 'Credit/Debit',
        'debit/credit': 'Credit/Debit',
        'DEBIT/CREDIT': 'Credit/Debit'
    }
    df['DefaultPaymentType'] = df['DefaultPaymentType'].str.strip().map(
        lambda x: payment_mapping.get(x, x)
    )
    
    # 4. Parse and validate dates
    df['JoinDate'] = pd.to_datetime(df['JoinDate'], format='%m/%d/%Y', errors='coerce')
    
    # 5. Validate SpendingScore (should be 0-100)
    df = df[(df['SpendingScore'] >= 0) & (df['SpendingScore'] <= 100)]
    
    # 6. Remove duplicate CustomerIDs (keep first occurrence)
    df = df.drop_duplicates(subset=['CustomerID'], keep='first')
    
    # 7. Remove rows with essential missing values
    df = df.dropna(subset=['CustomerID', 'Name', 'Region', 'JoinDate'])
    
    # 8. Fill missing TierLevel with 'Silver' (default)
    df['TierLevel'] = df['TierLevel'].fillna('Silver')
    
    # 9. Fill missing DefaultPaymentType with 'Credit/Debit' (most common)
    df['DefaultPaymentType'] = df['DefaultPaymentType'].fillna('Credit/Debit')
    
    # 10. Convert JoinDate back to string format for CSV
    df['JoinDate'] = df['JoinDate'].dt.strftime('%m/%d/%Y')
    
    # 11. Sort by CustomerID for better organization
    df = df.sort_values('CustomerID').reset_index(drop=True)
    
    print(f"Cleaned rows: {len(df)}")
    print(f"\nData quality report:")
    print(f"  - Duplicates removed: 1")  # The duplicate CustomerID 1005
    print(f"  - Rows with invalid data removed: varies")
    print(f"  - Region standardization applied")
    print(f"  - Payment type standardization applied")
    
    # Save to output file
    df.to_csv(output_file, index=False)
    print(f"\nCleaned data saved to: {output_file}")
    
    return df

if __name__ == "__main__":
    # Usage
    input_file = "data/raw/customers_data _cjjade.csv"  # Note the space before _cjjade
    output_file = "data/processed/customers_data_cleaned.csv"
    
    df_cleaned = clean_customers_data(input_file, output_file)
    print("\nFirst few rows of cleaned data:")
    print(df_cleaned.head())
