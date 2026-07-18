import pandas as pd
import re

# ============================================================
# 1. GENERIC HELPERS
# ============================================================

def read_csv_safe(path):
    """Read CSV using safe encoding."""
    return pd.read_csv(path, encoding="latin1")

def clean_text_columns(df):
    """Strip whitespace and remove weird characters."""
    df = df.replace({"\uFFFD": " ", "�": " "}, regex=True)
    df = df.apply(lambda col: col.astype(str).str.strip() if col.dtype == "object" else col)
    return df

def save(df, path):
    df.to_csv(path, index=False)
    print(f"Saved: {path}")

# ============================================================
# 2. PROCESS NUMERIC DATA (MELT YEARS)
# ============================================================

def process_numeric_data(path_in, path_out):
    df = read_csv_safe(path_in)

    # Identify year columns (numeric column names)
    year_cols = [col for col in df.columns if col.isdigit()]

    # Melt dataset
    df_melted = df.melt(
        id_vars=[col for col in df.columns if col not in year_cols],
        value_vars=year_cols,
        var_name="year",
        value_name="value"
    )

    # Ensure proper dtypes
    df_melted = df_melted.convert_dtypes()

    # Remove NULL / empty values safely
    df_melted = df_melted[df_melted["value"].notna()]
    df_melted = df_melted[df_melted["value"].astype(str).str.strip() != ""]

    save(df_melted, path_out)

# ============================================================
# 3. PROCESS COUNTRY-SERIES METADATA
# ============================================================

def extract_country_name(value):
    return re.sub(r"\s*\(.*?\)", "", str(value)).strip()

def extract_country_code(value):
    match = re.search(r"\((.*?)\)", str(value))
    return match.group(1) if match else None

def extract_series_name(value):
    return re.sub(r"\s*\(.*?\)", "", str(value)).strip()

def extract_series_code(value):
    match = re.search(r"\((.*?)\)", str(value))
    return match.group(1) if match else None

def process_country_series_metadata(path_in, path_out):
    df = read_csv_safe(path_in)

    if "Country Code" in df.columns:
        df["CountryName"] = df["Country Code"].apply(extract_country_name)
        df["CountryCode"] = df["Country Code"].apply(extract_country_code)

    if "Series Code" in df.columns:
        df["SeriesName"] = df["Series Code"].apply(extract_series_name)
        df["SeriesCode"] = df["Series Code"].apply(extract_series_code)

    if "Description" in df.columns:
        df["Description"] = df["Description"].astype(str).str.strip()

    clean_df = df[[
        "CountryName",
        "CountryCode",
        "SeriesName",
        "SeriesCode",
        "Description"
    ]]

    save(clean_df, path_out)

# ============================================================
# 4. PROCESS COUNTRY METADATA
# ============================================================

def process_country_metadata(path_in, path_out):
    df = read_csv_safe(path_in)

    df = df.dropna(how="all")
    df = clean_text_columns(df)

    if "Code" in df.columns:
        df = df[df["Code"].notnull()]

    save(df, path_out)

# ============================================================
# 5. PROCESS FOOTNOTE METADATA
# ============================================================

def process_footnote_metadata(path_in, path_out):
    df = read_csv_safe(path_in)

    df = df.dropna(how="all")
    df = clean_text_columns(df)

    if "SeriesCode" in df.columns and "CountryCode" in df.columns:
        df = df[(df["SeriesCode"].notnull()) | (df["CountryCode"].notnull())]

    save(df, path_out)

# ============================================================
# 6. PROCESS SERIES METADATA
# ============================================================

def process_series_metadata(path_in, path_out):
    df = read_csv_safe(path_in)

    df = df.dropna(how="all")
    df = clean_text_columns(df)

    if "SeriesCode" in df.columns:
        df = df[df["SeriesCode"].notnull()]

    save(df, path_out)

# ============================================================
# 7. RUN ALL PIPELINE STEPS
# ============================================================

def run_pipeline():
    print("Starting IDS Pipeline...\n")

    process_numeric_data(
        r"C:\Users\Ramya\dsproject-2\allcountries.csv",
        r"C:\Users\Ramya\dsproject-2\allcountries_cleaned.csv"
    )

    process_country_series_metadata(
        r"C:\Users\Ramya\dsproject-2\country_series.csv",
        r"C:\Users\Ramya\dsproject-2\country_series_Cleaned.csv"
    )

    process_country_metadata(
        r"C:\Users\Ramya\dsproject-2\country_metadata.csv",
        r"C:\Users\Ramya\dsproject-2\country_metaData_Cleaned.csv"
    )

    process_footnote_metadata(
       r"C:\Users\Ramya\dsproject-2\footnote_metadata.csv",
       r"C:\Users\Ramya\dsproject-2\footnote_metadata_Cleaned.csv"
    )

    process_series_metadata(
       r"C:\Users\Ramya\dsproject-2\series_metaData.csv",
       r"C:\Users\Ramya\dsproject-2\series_metadata_Cleaned.csv"
    )

    print("\nPipeline completed successfully.")

# ============================================================
# EXECUTE
# ============================================================

if __name__ == "__main__":
    run_pipeline()
