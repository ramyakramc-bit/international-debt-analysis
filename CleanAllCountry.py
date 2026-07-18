import pandas as pd
import re

# ============================================================
# 1. GENERIC HELPERS
# ============================================================

def normalize_columns(df):
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("__", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df

# ============================================================
# 2. CLEANERS
# ============================================================

# 1️⃣ ALL COUNTRIES (Numeric Data)
def clean_all_countries(file_path=r"C:\Users\Ramya\dsproject-2\allcountries_cleaned.csv"):
    print(f"\nCleaning All Countries: {file_path}")
    df = pd.read_csv(file_path)
    df = normalize_columns(df)

    required = ["country_code", "series_code", "year", "value"]
    existing = [c for c in required if c in df.columns]
    df = df[existing]

    df.to_csv(file_path, index=False)
    print("✔ Cleaned All Countries")

# 2️⃣ COUNTRY-SERIES METADATA
def clean_country_series(file_path=r"C:\Users\Ramya\dsproject-2\country_series_Cleaned.csv"):
    print(f"\nCleaning Country-Series Metadata: {file_path}")
    df = pd.read_csv(file_path)
    df = normalize_columns(df)

    required = ["countryname", "countrycode", "seriesname", "seriescode", "description"]
    existing = [c for c in required if c in df.columns]
    df = df[existing]

    df.to_csv(file_path, index=False)
    print("✔ Cleaned Country-Series Metadata")

# 3️⃣ COUNTRY METADATA
def clean_country_metadata(file_path=r"C:\Users\Ramya\dsproject-2\country_metaData_Cleaned.csv"):
    print(f"\nCleaning Country Metadata: {file_path}")
    df = pd.read_csv(file_path)
    df = normalize_columns(df)

    required = [
        "code","long_name","income_group","region","lending_category","other_groups",
        "currency_unit","latest_population_census","latest_household_survey",
        "special_notes","national_accounts_base_year","national_accounts_reference_year",
        "system_of_national_accounts","sna_price_valuation","ppp_survey_years",
        "balance_of_payments_manual_in_use","external_debt_reporting_status",
        "system_of_trade","government_accounting_concept",
        "imf_data_dissemination_standard",
        "source_of_most_recent_income_and_expenditure_data",
        "vital_registration_complete","latest_agricultural_census",
        "latest_industrial_data","latest_trade_data",
        "latest_water_withdrawal_data","2alpha_code","wb2_code",
        "table_name","short_name"
    ]
    existing = [c for c in required if c in df.columns]
    df = df[existing]

    df.to_csv(file_path, index=False)
    print("✔ Cleaned Country Metadata")

# 4️⃣ FOOTNOTE METADATA
def clean_footnotes(file_path=r"C:\Users\Ramya\dsproject-2\footnote_metadata_Cleaned.csv"):
    print(f"\nCleaning Footnotes: {file_path}")
    df = pd.read_csv(file_path)
    df = normalize_columns(df)

    required = ["country_code", "series_code", "time_code", "description"]
    existing = [c for c in required if c in df.columns]
    df = df[existing]

    df.to_csv(file_path, index=False)
    print("✔ Cleaned Footnotes")

# 5️⃣ SERIES METADATA
def clean_series_metadata(file_path=r"C:\Users\Ramya\dsproject-2\series_metadata_Cleaned.csv"):
    print(f"\nCleaning Series Metadata: {file_path}")
    df = pd.read_csv(file_path)
    df = normalize_columns(df)

    print("Columns found:", df.columns.tolist())

    possible = ["code", "series_code", "seriescode"]
    series_col = next((c for c in possible if c in df.columns), None)

    if series_col is None:
        print("❌ ERROR: No seriescode column found in Series Metadata")
        return

    df = df[df[series_col].notna() & (df[series_col].astype(str).str.strip() != "")]
    df = df.rename(columns={series_col: "seriescode"})

    required = [
        "seriescode",
        "indicator_name",
        "short_definition",
        "long_definition",
        "source",
        "topic",
        "dataset",
        "periodicity",
        "aggregation_method",
        "limitations_and_exceptions",
        "general_comments"
    ]
    existing = [c for c in required if c in df.columns]
    df = df[existing]

    df.to_csv(file_path, index=False)
    print("✔ Cleaned Series Metadata")

# ============================================================
# RUN ALL CLEANERS
# ============================================================

if __name__ == "__main__":
    clean_all_countries()
    clean_country_series()
    clean_country_metadata()
    clean_footnotes()
    clean_series_metadata()

