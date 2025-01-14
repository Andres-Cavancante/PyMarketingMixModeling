import pandas as pd

media_dt = pd.read_csv("/app/marketing_spend_and_revenue_data.csv")

media_vars = [
    "Google Performance Max",
    "Google Search Brand",
    "Google Search No Brand",
    "Facebook Conversions",
    "Facebook Others",
    "Facebook Product Catalog Sales",
    "Influencers",
    "Display Ads",
    "TV Ads",
    "Radio Ads",
    "Magazine Ads"
]

# media_vars = media_dt[media_vars]

correlation_matrix = media_dt.corr(numeric_only=True)

target_variable = "Revenue"

# target_variable = media_dt["Revenue"]

dependent_corr = correlation_matrix[target_variable].drop(target_variable).sort_values(ascending=False)

correlation_df = pd.DataFrame({
    "Variable": dependent_corr.index,
    "Correlation": dependent_corr.values
})

low_threshold = 0.2
high_threshold = 0.65

high_corr_df = correlation_df[correlation_df["Correlation"].abs() > high_threshold]
low_corr_df = correlation_df[correlation_df["Correlation"].abs() < low_threshold]

print("High Correlation Variables:")
print(high_corr_df)

print("\nLow Correlation Variables:")
print(low_corr_df)