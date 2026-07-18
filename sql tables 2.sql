
-- ============================================================
DROP TABLE IF EXISTS ids_all_countries;
DROP TABLE IF EXISTS ids_country_series_metadata;
DROP TABLE IF EXISTS ids_country_metadata;
DROP TABLE IF EXISTS ids_footnote_metadata;
DROP TABLE IF EXISTS ids_series_metadata;

-- ============================================================
-- 1. ids_all_countries  (Numeric Data)
-- ============================================================
CREATE TABLE ids_all_countries (
    country_code TEXT,
    series_code TEXT,
    year INTEGER,
    value NUMERIC
);

-- ============================================================
-- 2. ids_country_series_metadata
-- ============================================================
CREATE TABLE ids_country_series_metadata (
    countryname TEXT,
    countrycode TEXT,
    seriesname TEXT,
    seriescode TEXT,
    description TEXT
);

-- ============================================================
-- 3. ids_country_metadata
-- ============================================================

CREATE TABLE ids_country_metadata (
    code TEXT,
    long_name TEXT,
    income_group TEXT,
    region TEXT,
    lending_category TEXT,
    other_groups TEXT,
    currency_unit TEXT,
    latest_population_census TEXT,
    latest_household_survey TEXT,
    special_notes TEXT,
    national_accounts_base_year TEXT,
    national_accounts_reference_year TEXT,
    system_of_national_accounts TEXT,
    sna_price_valuation TEXT,
    ppp_survey_years TEXT,
    balance_of_payments_manual_in_use TEXT,
    external_debt_reporting_status TEXT,
    system_of_trade TEXT,
    government_accounting_concept TEXT,
    imf_data_dissemination_standard TEXT,
    source_of_most_recent_income_and_expenditure_data TEXT,
    vital_registration_complete TEXT,
    latest_agricultural_census TEXT,
    latest_industrial_data TEXT,
    latest_trade_data TEXT,
    latest_water_withdrawal_data TEXT,
    table_name TEXT,
    short_name TEXT
);

-- ============================================================
-- 4. ids_footnote_metadata
-- ============================================================
CREATE TABLE ids_footnote_metadata (
    country_code TEXT,
    series_code TEXT,
    time_code TEXT,
    description TEXT
);

-- ============================================================
-- 5. ids_series_metadata
-- ============================================================
CREATE TABLE ids_series_metadata (
    seriescode TEXT,
    indicator_name TEXT,
    short_definition TEXT,
    long_definition TEXT,
    source TEXT,
    topic TEXT,
    dataset TEXT,
    periodicity TEXT,
    aggregation_method TEXT,
    limitations_and_exceptions TEXT,
    general_comments TEXT
);




