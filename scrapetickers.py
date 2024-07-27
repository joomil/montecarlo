import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the web page
url = "https://companiesmarketcap.com/france/largest-companies-in-france-by-market-cap/"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 3: Find all div elements with the class 'company-code'
    company_codes = soup.find_all('div', class_='company-code')
    
    # Step 4: Extract and print the text inside each div
    for code in company_codes:
        print(code.get_text(strip=True))
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
