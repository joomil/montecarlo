import time
import csv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup

# Step 1: Set up WebDriver with WebDriver Manager
service = FirefoxService(GeckoDriverManager().install())
options = Options()
driver = webdriver.Firefox(service=service, options=options)

# Step 2: Open the URL of the first page
base_url = "https://companiesmarketcap.com/page/"
page_number = 1
all_data = []

while True:
    url = f"{base_url}{page_number}/"
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    # Step 3: Automatically scroll the page
    scroll_pause_time = 2  # Pause between each scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
    i = 1

    while True:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)

        # Check if reaching the end of the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break

    # Step 4: Fetch the data using BeautifulSoup after all data is loaded
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Step 5: Find all div elements with the class 'company-code'
    company_codes = soup.find_all('div', class_='company-code')

    # Step 6: Extract the text inside each div
    for code in company_codes:
        text = code.get_text(strip=True)
        all_data.append([text])

    # Check if there is a next page
    next_button = soup.find('a', class_='next page-numbers')
    if not next_button:
        break

    page_number += 1

# Step 7: Save the data to a CSV file
with open('company_codes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Code'])  # Write the header
    writer.writerows(all_data)  # Write the data

print("Data has been saved to company_codes.csv successfully!")

# Close the WebDriver session
driver.quit()
