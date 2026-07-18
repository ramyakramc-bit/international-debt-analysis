import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import altair as alt

# ---------------------------------------------------------
# 1. Database Connection
# ---------------------------------------------------------
host = "localhost"
database = "my_db"
user = "postgres"
password = "genetics"

engine = create_engine(
    f"postgresql://{user}:{password}@{host}:5432/{database}"
)

# ---------------------------------------------------------
# 2. Helper Functions
# ---------------------------------------------------------
def load_table(table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)

@st.cache_data
def load_all_data():
    df_all = load_table("ids_all_countries")
    df_country = load_table("ids_country_metadata")
    df_series = load_table("ids_series_metadata")
    return df_all, df_country, df_series

df_all, df_country, df_series = load_all_data()

#st.write("DF_ALL Columns:", df_all.columns.tolist())
#st.write("DF_SERIES Columns:", df_series.columns.tolist())
#st.write("DF_COUNTRY Columns:", df_country.columns.tolist())

# ---------------------------------------------------------
# 3. App Title
# ---------------------------------------------------------
st.title("📊 International Debt Statistics — Insights Dashboard")
#st.write("Supabase + Streamlit + IDS")

# ---------------------------------------------------------
# 4. Country-wise Debt Distribution
# ---------------------------------------------------------
st.header(" Country-wise Debt Distribution")

country_debt = (
    df_all.groupby("country_code")["value"]
    .sum()
    .reset_index()
    .sort_values("value", ascending=False)
)

chart_country = (
    alt.Chart(country_debt.head(20))
    .mark_bar()
    .encode(
        x=alt.X("country_code:N", sort="-y", title="Country"),
        y=alt.Y("value:Q", title="Total Debt"),
        tooltip=["country_code", "value"]
    )
)

st.altair_chart(chart_country, use_container_width=True)

# ---------------------------------------------------------
# 5. Top & Bottom Countries
# ---------------------------------------------------------
st.header("🏆 Top & Bottom Countries by Debt")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Countries")
    st.dataframe(country_debt.head(10))

with col2:
    st.subheader("Bottom 10 Countries")
    st.dataframe(country_debt.tail(10))

# ---------------------------------------------------------
# 6. Debt Distribution Across Indicators
# ---------------------------------------------------------
st.header("📈 Debt Distribution Across Indicators")

df_join = df_all.merge(
    df_series,
    left_on="series_code",
    right_on="series_code",
    how="left"
)

indicator_summary = (
    df_join.groupby("indicator_name")["value"]
    .sum()
    .reset_index()
    .sort_values("value", ascending=False)
)

chart_indicator = (
    alt.Chart(indicator_summary.head(20))
    .mark_bar()
    .encode(
        x=alt.X("indicator_name:N", sort="-y", title="Indicator"),
        y=alt.Y("value:Q", title="Total Debt"),
        tooltip=["indicator_name", "value"]
    )
)

st.altair_chart(chart_indicator, use_container_width=True)

# ---------------------------------------------------------
# 7. Global Debt Trend Over Time
# ---------------------------------------------------------
st.header("📅 Global Debt Trend Over Time")

year_trend = (
    df_all.groupby("year")["value"]
    .sum()
    .reset_index()
    .sort_values("year")
)

chart_trend = (
    alt.Chart(year_trend)
    .mark_line(point=True)
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("value:Q", title="Total Debt"),
        tooltip=["year", "value"]
    )
)

st.altair_chart(chart_trend, use_container_width=True)

# ---------------------------------------------------------
# 8. Country-specific Trend
# ---------------------------------------------------------
st.header("🔍 Country-specific Debt Trend")

country_list = sorted(df_all["country_code"].unique())
selected_country = st.selectbox("Select a country", country_list)

trend_country = (
    df_all[df_all["country_code"] == selected_country]
    .groupby("year")["value"]
    .sum()
    .reset_index()
    .sort_values("year")
)

chart_country_trend = (
    alt.Chart(trend_country)
    .mark_line(point=True)
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("value:Q", title="Total Debt"),
        tooltip=["year", "value"]
    )
)

st.altair_chart(chart_country_trend, use_container_width=True)

# ---------------------------------------------------------
# 9. Statistical Summary
# ---------------------------------------------------------
st.header("📐 Statistical Summary of Debt Values")
st.write(df_all["value"].describe())

# ---------------------------------------------------------
# SQL Queries Section
# ---------------------------------------------------------

# 1 Distinct country names
df_countries = pd.read_sql("""
    SELECT DISTINCT m.short_name AS country_name
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
""", engine)
st.header("Distinct Country Names")
st.dataframe(df_countries)

# 2 Count total countries
df_total_countries = pd.read_sql("""
    SELECT COUNT(DISTINCT a.country_code) AS total_countries
    FROM ids_all_countries a
""", engine)
st.header("Total Number of Countries")
st.dataframe(df_total_countries)

# 3 Count total indicators
df_total_indicators = pd.read_sql("""
    SELECT COUNT(DISTINCT s.series_code) AS total_indicators
    FROM ids_all_countries a
    JOIN ids_series_metadata s ON a.series_code = s.series_code
""", engine)
st.header("Total Number of Indicators")
st.dataframe(df_total_indicators)

# 4 First 10 records
df_first10 = pd.read_sql("SELECT * FROM ids_all_countries LIMIT 10;", engine)
st.header("First 10 Records")
st.dataframe(df_first10)

# 5 Total global debt
df_total_global_debt = pd.read_sql("""
    SELECT SUM(value) AS total_global_debt
    FROM ids_all_countries
""", engine)
st.header("Total Global Debt")
st.dataframe(df_total_global_debt)

# 6 Unique indicator names
df_unique_indicators = pd.read_sql("""
    SELECT DISTINCT s.indicator_name AS indicator_name
    FROM ids_all_countries a
    JOIN ids_series_metadata s ON a.series_code = s.series_code
""", engine)
st.header("Unique Indicator Names")
st.dataframe(df_unique_indicators)

# 7 Number of records per country
df_country_records = pd.read_sql("""
    SELECT m.short_name AS country_name, COUNT(*) AS record_count
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    ORDER BY record_count DESC
""", engine)
st.header("Number of Records for Each Country")
st.dataframe(df_country_records)

# 8 Debt > 1 billion
df_high_debt = pd.read_sql("""
    SELECT *
    FROM ids_all_countries
    WHERE value > 1000000000
""", engine)
st.header("Records with Debt Greater than 1 Billion USD")
st.dataframe(df_high_debt)

# 9 Min, Max, Avg debt
df_debt_stats = pd.read_sql("""
    SELECT MIN(value) AS min_debt,
           MAX(value) AS max_debt,
           AVG(value) AS avg_debt
    FROM ids_all_countries
""", engine)
st.header("Debt Value Statistics")
st.dataframe(df_debt_stats)

# 10 Total records
df_total_records = pd.read_sql("""
    SELECT COUNT(*) AS total_records
    FROM ids_all_countries
""", engine)
st.header("Total Number of Records")
st.dataframe(df_total_records)

# 11 Total debt by country
df_total_debt_by_country = pd.read_sql("""
    SELECT m.short_name AS country_name, SUM(a.value) AS total_debt
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    ORDER BY total_debt DESC
""", engine)
st.header("Total Debt by Country")
st.dataframe(df_total_debt_by_country)

# 12 Top 10 countries by debt
df_top_10_countries = pd.read_sql("""
    SELECT m.short_name AS country_name, SUM(a.value) AS total_debt
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    ORDER BY total_debt DESC
    LIMIT 10
""", engine)
st.header("Top 10 Countries by Total Debt")
st.dataframe(df_top_10_countries)

# 13 Average debt per country
df_avg_debt_by_country = pd.read_sql("""
    SELECT m.short_name AS country_name, AVG(a.value) AS avg_debt
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    ORDER BY avg_debt DESC
""", engine)
st.header("Average Debt by Country")
st.dataframe(df_avg_debt_by_country)

# 14 Total debt per indicator
df_total_debt_by_indicator = pd.read_sql("""
    SELECT s.indicator_name AS indicator_name, SUM(a.value) AS total_debt
    FROM ids_all_countries a
    JOIN ids_series_metadata s ON a.series_code = s.series_code
    GROUP BY s.indicator_name
    ORDER BY total_debt DESC
""", engine)
st.header("Total Debt by Indicator")
st.dataframe(df_total_debt_by_indicator)

# 15 Indicator with highest debt
df_highest_debt_indicator = pd.read_sql("""
    SELECT s.indicator_name AS indicator_name, SUM(a.value) AS total_debt
    FROM ids_all_countries a
    JOIN ids_series_metadata s ON a.series_code = s.series_code
    GROUP BY s.indicator_name
    ORDER BY total_debt DESC
    LIMIT 1
""", engine)
st.header("Indicator with Highest Total Debt")
st.dataframe(df_highest_debt_indicator)

# 16 Country with lowest debt
df_lowest_debt_country = pd.read_sql("""
    SELECT m.short_name AS country_name, SUM(a.value) AS total_debt
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    ORDER BY total_debt ASC
    LIMIT 1
""", engine)
st.header("Country with Lowest Total Debt")
st.dataframe(df_lowest_debt_country)

# 17 Debt per country & indicator
df_total_debt_by_country_indicator = pd.read_sql("""
    SELECT m.short_name AS country_name, s.indicator_name AS indicator_name, SUM(a.value) AS total_debt
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    JOIN ids_series_metadata s ON a.series_code = s.series_code
    GROUP BY m.short_name, s.indicator_name
    ORDER BY m.short_name, total_debt DESC
""", engine)
st.header("Total Debt by Country and Indicator")
st.dataframe(df_total_debt_by_country_indicator)

# 18 Indicator count per country
df_indicator_count_by_country = pd.read_sql("""
    SELECT m.short_name AS country_name, COUNT(DISTINCT s.series_code) AS indicator_count
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    JOIN ids_series_metadata s ON a.series_code = s.series_code
    GROUP BY m.short_name
    ORDER BY indicator_count DESC
""", engine)
st.header("Indicator Count by Country")
st.dataframe(df_indicator_count_by_country)

# 19 Countries above global average
df_countries_above_average = pd.read_sql("""
    SELECT m.short_name AS country_name, SUM(a.value) AS total_debt
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    HAVING SUM(a.value) > (
        SELECT AVG(total_debt)
        FROM (
            SELECT SUM(value) AS total_debt
            FROM ids_all_countries
            GROUP BY country_code
        ) subquery
    )
    ORDER BY total_debt DESC
""", engine)
st.header("Countries with Debt Above Global Average")
st.dataframe(df_countries_above_average)

# 20 Rank countries by debt
df_ranked_countries = pd.read_sql("""
    SELECT m.short_name AS country_name,
           SUM(a.value) AS total_debt,
           RANK() OVER (ORDER BY SUM(a.value) DESC) AS debt_rank
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    ORDER BY debt_rank
""", engine)
st.header("Ranked Countries by Total Debt")
st.dataframe(df_ranked_countries)

# 21 Top 5 indicators contributing most to global debt
df_top_indicators = pd.read_sql("""
    SELECT s.indicator_name AS indicator_name, SUM(a.value) AS total_debt
    FROM ids_all_countries a
    JOIN ids_series_metadata s ON a.series_code = s.series_code
    GROUP BY s.indicator_name
    ORDER BY total_debt DESC
    LIMIT 5
""", engine)
st.header("Top 5 Indicators Contributing to Global Debt")
st.dataframe(df_top_indicators)

# 22 Percentage contribution of each country
df_percentage_contribution = pd.read_sql("""
    SELECT m.short_name AS country_name,
           (SUM(a.value) * 100.0 / (SELECT SUM(value) FROM ids_all_countries)) AS percentage_contribution
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    ORDER BY percentage_contribution DESC
""", engine)
st.header("Percentage Contribution of Each Country to Global Debt")
st.dataframe(df_percentage_contribution)

# 23 Top 3 countries for each indicator
df_top_countries_per_indicator = pd.read_sql("""
WITH ranked AS (
    SELECT 
        s.indicator_name,
        m.short_name AS country_name,
        SUM(a.value) AS total_debt,
        RANK() OVER (
            PARTITION BY s.indicator_name 
            ORDER BY SUM(a.value) DESC
        ) AS rank
    FROM ids_all_countries a
    JOIN ids_country_metadata m 
        ON a.country_code = m.code
    JOIN ids_series_metadata s 
        ON a.series_code = s.series_code
    GROUP BY s.indicator_name, m.short_name, a.country_code
)
SELECT *
FROM ranked
WHERE rank <= 3
ORDER BY indicator_name, rank;
""", engine)
st.header("Top 3 Countries for Each Indicator Based on Debt")
st.dataframe(df_top_countries_per_indicator)

# 24 Debt range per country
df_debt_range = pd.read_sql("""
    SELECT m.short_name AS country_name,
           MAX(a.value) - MIN(a.value) AS debt_range
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    ORDER BY debt_range DESC
""", engine)
st.header("Debt Range (Max - Min) per Country")
st.dataframe(df_debt_range)

# 25 View for top 10 countries
from sqlalchemy import text
with engine.begin() as conn:
    conn.execute(text("""
        CREATE OR REPLACE VIEW top10_countries_debt AS
        SELECT m.short_name AS country_name, SUM(a.value) AS total_debt
        FROM ids_all_countries a
        JOIN ids_country_metadata m ON a.country_code = m.code
        GROUP BY m.short_name
        ORDER BY total_debt DESC
        LIMIT 10
    """))
df_top10_countries_debt = pd.read_sql("SELECT * FROM top10_countries_debt;", engine)
st.header("Top 10 Countries with Highest Debt (View)")
st.dataframe(df_top10_countries_debt)


# 26 Categorize countries
df_categorize_countries = pd.read_sql("""
    SELECT m.short_name AS country_name,
           SUM(a.value) AS total_debt,
           CASE
               WHEN SUM(a.value) > 1000000 THEN 'High Debt'
               WHEN SUM(a.value) BETWEEN 500000 AND 1000000 THEN 'Medium Debt'
               ELSE 'Low Debt'
           END AS debt_category
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    ORDER BY total_debt DESC
""", engine)
st.header("Debt Category by Country")
st.dataframe(df_categorize_countries)

# 27 Cumulative debt per country
df_cumulative_debt = pd.read_sql("""
    SELECT m.short_name AS country_name,
           a.year,
           SUM(a.value) OVER (PARTITION BY a.country_code ORDER BY a.year) AS cumulative_debt
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    ORDER BY m.short_name, a.year
""", engine)
st.header("Cumulative Debt per Country Over Years")
st.dataframe(df_cumulative_debt)

# 28 Indicators with higher avg debt
df_higher_avg_debt = pd.read_sql("""
    SELECT s.indicator_name,
           AVG(a.value) AS avg_debt
    FROM ids_all_countries a
    JOIN ids_series_metadata s ON a.series_code = s.series_code
    GROUP BY s.indicator_name
    HAVING AVG(a.value) > (SELECT AVG(value) FROM ids_all_countries)
    ORDER BY avg_debt DESC
""", engine)
st.header("Indicators with Average Debt Higher than Overall Average")
st.dataframe(df_higher_avg_debt)

# 29 Countries contributing > 5%
df_countries_high_contribution = pd.read_sql("""
    SELECT m.short_name AS country_name,
           SUM(a.value) AS total_debt,
           (SUM(a.value) * 100.0 / (SELECT SUM(value) FROM ids_all_countries)) AS percentage_contribution
    FROM ids_all_countries a
    JOIN ids_country_metadata m ON a.country_code = m.code
    GROUP BY m.short_name
    HAVING (SUM(a.value) * 100.0 / (SELECT SUM(value) FROM ids_all_countries)) > 5
    ORDER BY percentage_contribution DESC
""", engine)
st.header("Countries Contributing More than 5% of Global Debt")
st.dataframe(df_countries_high_contribution)
