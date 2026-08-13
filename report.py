# ── AI Market Report Generator ──────────────────────────────────
# This file takes the analysis results from analyze.py and sends
# them to the Claude API to generate a plain-language market report
# that a non-technical landlord could actually read and act on.

import os
from dotenv import load_dotenv
import anthropic

# load_dotenv() reads your .env file and makes the API key available
# to your code as an environment variable — this is the standard
# safe way to use secret keys in Python
load_dotenv()

# Initialize the Anthropic client
# It automatically looks for ANTHROPIC_API_KEY in your environment
client = anthropic.Anthropic()

def generate_market_report(stats: dict) -> str:
    """
    Takes a dictionary of market stats and asks Claude to write
    a plain-language report a landlord could actually use.
    
    In Python, a dict is like a labeled container:
    {'median_rent': 1715, 'mean_rent': 1916}
    You access values with stats['median_rent']
    """
    
    # This is the prompt we send to Claude — we're injecting our
    # real data into the text using f-strings (f"..." lets you
    # embed variables directly in a string with {variable_name})
    prompt = f"""
    You are a real estate market analyst. Based on the following 
    rental market data for California, write a clear, actionable 
    market report for a small landlord or property manager.
    
    The report should be conversational, practical, and under 300 words.
    Focus on what a landlord should actually do with this information.
    
    MARKET DATA:
    - Total California listings analyzed: {stats['total_listings']:,}
    - Median rent: ${stats['median_rent']:,}/month
    - Mean rent: ${stats['mean_rent']:,}/month
    - Standard deviation: ${stats['std_rent']:,}
    - 25th percentile: ${stats['p25_rent']:,}/month
    - 75th percentile: ${stats['p75_rent']:,}/month
    
    RENT BY BEDROOM COUNT:
    - 1 bed: ${stats['rent_1bed']:,}/month median
    - 2 bed: ${stats['rent_2bed']:,}/month median  
    - 3 bed: ${stats['rent_3bed']:,}/month median
    - 4 bed: ${stats['rent_4bed']:,}/month median
    
    A/B TEST FINDING:
    - Furnished units rent for ${stats['furnished_premium']:,}/month MORE
      than unfurnished units
    - This difference is statistically significant (p < 0.0001)
    - Furnished median: ${stats['furnished_median']:,}/month
    - Unfurnished median: ${stats['unfurnished_median']:,}/month
    
    Write the report now:
    """
    
    # This is the actual API call — we send the prompt to Claude
    # and get back a response object
    message = client.messages.create(
        model="claude-sonnet-4-6",   # the model we're using
        max_tokens=1024,              # max length of the response
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # The response comes back as an object — we dig into it to get
    # the actual text string
    return message.content[0].text


# ── Run it ──────────────────────────────────────────────────────
# These are the stats from our analyze.py output — we're hardcoding
# them here for now. Later we'll connect the two files automatically.

stats = {
    'total_listings': 31126,
    'median_rent': 1715,
    'mean_rent': 1916,
    'std_rent': 909,
    'p25_rent': 1340,
    'p75_rent': 2250,
    'rent_1bed': 1616,
    'rent_2bed': 1705,
    'rent_3bed': 1850,
    'rent_4bed': 2395,
    'furnished_premium': 600,
    'furnished_median': 2300,
    'unfurnished_median': 1700,
}

print("Generating AI market report...\n")
report = generate_market_report(stats)
print("── AI MARKET REPORT ────────────────────────────────────")
print(report)
print("────────────────────────────────────────────────────────")