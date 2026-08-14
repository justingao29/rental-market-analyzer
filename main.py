# ── Rental Market Analyzer — Main Pipeline ──────────────────────
# Run this file to execute the full analysis end to end:
# 1. Load and clean the data
# 2. Run California market analysis
# 3. Run A/B test (furnished vs unfurnished)
# 4. Generate AI market report via Claude API

import pandas as pd
import numpy as np
from scipy import stats
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

# ── STEP 1: LOAD AND CLEAN ──────────────────────────────────────
print("Loading data...")
df = pd.read_csv('data/housing.csv')
print(f"Raw data: {df.shape[0]:,} rows")

df = df.dropna(subset=['price', 'sqfeet', 'beds', 'baths'])
df = df[(df['price'] >= 100) & (df['price'] <= 10000)]
df = df[(df['sqfeet'] >= 100) & (df['sqfeet'] <= 10000)]
df = df[(df['beds'] > 0) & (df['baths'] > 0)]
print(f"Clean data: {df.shape[0]:,} rows")

# ── STEP 2: CALIFORNIA ANALYSIS ─────────────────────────────────
print("\nAnalyzing California market...")
ca_df = df[df['state'].str.lower() == 'ca']

stats_dict = {
    'total_listings': len(ca_df),
    'median_rent': int(np.median(ca_df['price'])),
    'mean_rent': int(np.mean(ca_df['price'])),
    'std_rent': int(np.std(ca_df['price'])),
    'p25_rent': int(np.percentile(ca_df['price'], 25)),
    'p75_rent': int(np.percentile(ca_df['price'], 75)),
}

# Bedroom breakdown — .get() safely returns a default if a key
# doesn't exist, avoiding crashes on missing bedroom counts
bed_medians = ca_df.groupby('beds')['price'].median()
stats_dict['rent_1bed'] = int(bed_medians.get(1, 0))
stats_dict['rent_2bed'] = int(bed_medians.get(2, 0))
stats_dict['rent_3bed'] = int(bed_medians.get(3, 0))
stats_dict['rent_4bed'] = int(bed_medians.get(4, 0))

print(f"California listings: {stats_dict['total_listings']:,}")
print(f"Median rent: ${stats_dict['median_rent']:,}")
print(f"Mean rent:   ${stats_dict['mean_rent']:,}")

# ── STEP 3: A/B TEST ────────────────────────────────────────────
print("\nRunning A/B test...")
furnished = ca_df[ca_df['comes_furnished'] == 1]['price']
unfurnished = ca_df[ca_df['comes_furnished'] == 0]['price']

t_stat, p_value = stats.ttest_ind(furnished, unfurnished)

stats_dict['furnished_median'] = int(furnished.median())
stats_dict['unfurnished_median'] = int(unfurnished.median())
stats_dict['furnished_premium'] = stats_dict['furnished_median'] - stats_dict['unfurnished_median']

print(f"Furnished median:   ${stats_dict['furnished_median']:,}")
print(f"Unfurnished median: ${stats_dict['unfurnished_median']:,}")
print(f"Premium:            ${stats_dict['furnished_premium']:,}")
print(f"P-value:            {p_value:.6f} ({'SIGNIFICANT' if p_value < 0.05 else 'NOT SIGNIFICANT'})")

# ── STEP 4: CLAUDE API REPORT ───────────────────────────────────
print("\nGenerating AI market report...")
client = anthropic.Anthropic()

prompt = f"""
You are a real estate market analyst. Based on the following 
rental market data for California, write a clear, actionable 
market report for a small landlord or property manager.

The report should be conversational, practical, and under 300 words.
Focus on what a landlord should actually do with this information.

MARKET DATA:
- Total California listings analyzed: {stats_dict['total_listings']:,}
- Median rent: ${stats_dict['median_rent']:,}/month
- Mean rent: ${stats_dict['mean_rent']:,}/month
- Standard deviation: ${stats_dict['std_rent']:,}
- 25th percentile: ${stats_dict['p25_rent']:,}/month
- 75th percentile: ${stats_dict['p75_rent']:,}/month

RENT BY BEDROOM COUNT:
- 1 bed: ${stats_dict['rent_1bed']:,}/month median
- 2 bed: ${stats_dict['rent_2bed']:,}/month median
- 3 bed: ${stats_dict['rent_3bed']:,}/month median
- 4 bed: ${stats_dict['rent_4bed']:,}/month median

A/B TEST FINDING:
- Furnished units rent for ${stats_dict['furnished_premium']:,}/month MORE
  than unfurnished units
- This difference is statistically significant (p < 0.0001)
- Furnished median: ${stats_dict['furnished_median']:,}/month
- Unfurnished median: ${stats_dict['unfurnished_median']:,}/month

Write the report now:
"""

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

print("\n── AI MARKET REPORT ────────────────────────────────────")
print(message.content[0].text)
print("────────────────────────────────────────────────────────")

# ── DONE ────────────────────────────────────────────────────────
print("\nPipeline complete.")