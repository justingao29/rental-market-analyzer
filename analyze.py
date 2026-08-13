# ── Rental Market Analyzer ──────────────────────────────────────
# Step 1: Load and explore the data
#
# In Python, lines starting with # are comments — they don't run,
# they just explain what the code is doing. You'll see a lot of
# these as we build.

import pandas as pd        # pd is just a shorthand nickname — everyone uses it
import numpy as np         # same here, np is the standard nickname for numpy

# Load the dataset
df = pd.read_csv('data/housing.csv')

print(f"Raw data: {df.shape[0]:,} rows")

# ── CLEANING ────────────────────────────────────────────────────
# Real data is always dirty. We need to remove garbage rows before
# we can trust any analysis.

# Step 1: Drop rows where price or sqfeet are missing
# .dropna() removes rows that have NaN (empty) values in those columns
df = df.dropna(subset=['price', 'sqfeet', 'beds', 'baths'])

# Step 2: Filter out unrealistic prices
# A real rental is between $100 and $10,000/month
# Boolean filtering in pandas works like this:
# df[condition] returns only the rows where condition is True
df = df[(df['price'] >= 100) & (df['price'] <= 10000)]

# Step 3: Filter out unrealistic square footage
# Real rentals are between 100 and 10,000 sqft
df = df[(df['sqfeet'] >= 100) & (df['sqfeet'] <= 10000)]

# Step 4: Filter out zero beds/baths
df = df[(df['beds'] > 0) & (df['baths'] > 0)]

print(f"Clean data: {df.shape[0]:,} rows")
print(f"Removed: {384977 - df.shape[0]:,} bad rows")

# ── ANALYSIS ────────────────────────────────────────────────────
# Now let's look at California specifically since that's your market
# .str.lower() makes the comparison case-insensitive
ca_df = df[df['state'].str.lower() == 'ca']

print(f"\nCalifornia listings: {ca_df.shape[0]:,}")

# NumPy and pandas stats on California rent prices
print(f"\n── California Rent Stats ──")
print(f"Mean rent:    ${np.mean(ca_df['price']):,.0f}")
print(f"Median rent:  ${np.median(ca_df['price']):,.0f}")
print(f"Std dev:      ${np.std(ca_df['price']):,.0f}")
print(f"25th pctile:  ${np.percentile(ca_df['price'], 25):,.0f}")
print(f"75th pctile:  ${np.percentile(ca_df['price'], 75):,.0f}")

# ── BREAKDOWN BY BEDS ───────────────────────────────────────────
# .groupby() is one of pandas' most powerful tools
# It groups rows by a column and lets you run calculations on each group
# Think of it like a pivot table in Excel
print(f"\n── Median Rent by Bedroom Count (CA) ──")
bed_summary = ca_df.groupby('beds')['price'].agg(['median', 'mean', 'count'])
bed_summary.columns = ['Median Rent', 'Mean Rent', 'Count']
print(bed_summary)

# ── A/B TEST ────────────────────────────────────────────────────
# Question: Do furnished units rent for significantly more than
# unfurnished ones in California?
#
# This is A/B testing — we have two groups (furnished vs unfurnished)
# and we want to know if the difference in rent is real or just
# random noise in the data.
#
# We use a t-test to answer this. A t-test compares the means of
# two groups and tells you the probability that the difference
# happened by chance. That probability is the p-value.
#
# Standard rule: if p-value < 0.05, the difference is statistically
# significant — meaning it's almost certainly real, not random.

from scipy import stats   # scipy has the t-test built in

# Split into two groups
# remember: comes_furnished is 1 (yes) or 0 (no)
furnished = ca_df[ca_df['comes_furnished'] == 1]['price']
unfurnished = ca_df[ca_df['comes_furnished'] == 0]['price']

print(f"\n── A/B Test: Furnished vs Unfurnished (CA) ──")
print(f"Furnished listings:   {len(furnished):,}")
print(f"Unfurnished listings: {len(unfurnished):,}")
print(f"Median furnished:     ${furnished.median():,.0f}")
print(f"Median unfurnished:   ${unfurnished.median():,.0f}")
print(f"Difference:           ${furnished.median() - unfurnished.median():,.0f}")

# Run the t-test
# ttest_ind compares two independent groups
# it returns two things: the t-statistic and the p-value
t_stat, p_value = stats.ttest_ind(furnished, unfurnished)

print(f"\nT-statistic: {t_stat:.4f}")
print(f"P-value:     {p_value:.6f}")

if p_value < 0.05:
    print("\nResult: STATISTICALLY SIGNIFICANT")
    print("Furnished units rent for a meaningfully different amount.")
    print("This difference is almost certainly real, not random.")
else:
    print("\nResult: NOT STATISTICALLY SIGNIFICANT")
    print("We can't confidently say furnished units rent for more.")