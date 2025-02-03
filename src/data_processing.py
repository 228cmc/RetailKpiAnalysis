import pandas as pd
import os

def clean_data(file_path):
    """
    Cleans the raw data from the CSV file.
    Args:
        file_path (str): Path to the raw CSV file.
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Load data
    df = pd.read_csv(file_path)

    # Expected column names (ensuring order matches PostgreSQL table)
    required_columns = ['sale_date', 'company_name', 'total_sales', 'web_traffic', 'ad_spend',
                        'customer_reviews', 'social_media_mentions']

    # Check if all required columns exist
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in CSV: {missing_columns}")

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df['web_traffic'] = df['web_traffic'].fillna(0)
    df['ad_spend'] = df['ad_spend'].fillna(0)
    df['customer_reviews'] = df['customer_reviews'].fillna(3.0)  # Default average review score

    # Convert date column to datetime
    df['sale_date'] = pd.to_datetime(df['sale_date'])

    # Ensure column order matches PostgreSQL table
    df = df[['sale_date', 'company_name', 'total_sales', 'web_traffic', 
             'ad_spend', 'customer_reviews', 'social_media_mentions']]

    return df

if __name__ == "__main__":
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "data", "raw", "retail_data.csv")
    output_path = os.path.join(base_dir, "data", "processed", "retail_cleaned.csv")

    # Process data
    cleaned_data = clean_data(input_path)
    cleaned_data.to_csv(output_path, index=False)

    print(f" Data cleaned and saved to '{output_path}'.")
