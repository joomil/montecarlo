import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Fetch the web page
url = "https://companiesmarketcap.com/"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 3: Find all div elements with the class 'company-code'
    company_codes = soup.find_all('div', class_='company-code')
    
    # Step 4: Extract the text inside each div
    data = []
    for code in company_codes:
        text = code.get_text(strip=True)
        data.append([text])
    
    # Step 5: Save the data to a CSV file
    with open('company_codes.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Code'])  # Write the header
        writer.writerows(data)  # Write the data

    print("Data has been saved to company_codes.csv successfully!")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
