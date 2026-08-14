# Rental Market Analyzer

An AI-powered rental market analysis tool that processes real 
Craigslist listing data and generates plain-language market reports 
for landlords and property managers using the Claude API.

## What It Does

- Cleans and analyzes 385,000+ real rental listings from across the US
- Generates California market statistics (median rent, percentiles, 
  bedroom breakdowns)
- Runs a statistically significant A/B test comparing furnished vs 
  unfurnished unit pricing
- Uses the Claude API to produce actionable plain-language market 
  reports a non-technical landlord can actually use

## Key Findings (California Market)

- Median rent: $1,715/month across 31,000+ listings
- Furnished units command a **$600/month premium** over unfurnished 
  (statistically significant, p < 0.0001)
- At $600/month premium, furnishing costs recoup in 5-13 months

## Tools Used

- Python
- pandas — data cleaning and analysis
- NumPy — statistical calculations
- SciPy — hypothesis testing (t-test)
- Anthropic Claude API — AI-generated market reports

## Setup

1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip3 install pandas numpy scipy anthropic python-dotenv`
5. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/austinreese/usa-housing-listings) 
   and place `housing.csv` in a `/data` folder
6. Create a `.env` file with your Claude API key:
   `ANTHROPIC_API_KEY=your-key-here`
7. Run the full pipeline: python3 main.py

## Sample Output

```
── California Rent Stats ──
Mean rent:    $1,916
Median rent:  $1,715
Std dev:      $909
25th pctile:  $1,340
75th pctile:  $2,250

── A/B Test: Furnished vs Unfurnished ──
Median furnished:     $2,300
Median unfurnished:   $1,700
Difference:           $600
P-value:     0.000000
Result: STATISTICALLY SIGNIFICANT
```