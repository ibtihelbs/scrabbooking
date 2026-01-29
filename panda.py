import pandas as pd
import requests

# URL of the Simpsons episodes page
url = 'https://www.football-data.co.uk/mmz4281/2526/I1.csv'

# # Set a User-Agent so Wikipedia doesn't block us
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# # Fetch the HTML
# html = requests.get(url, headers=headers).text

# # Parse all tables
# tables = pd.read_html(html, flavor='html5lib')

# # How many tables were found
# print(f"Found {len(tables)} tables.")

# # Show the first 5 rows of the first table
# print(tables[0].head())

data = pd.read_csv(url)
print(data.head())