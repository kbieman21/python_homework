# Task 6: Scraping Structured Data

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# Setup browser options
options = Options()
options.add_argument("--headless")  # Remove this line to see the browser window for debugging
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Educational Scraper - Bootcamp Project)")


# Auto-manage driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Target URL from Task 2
url = "https://owasp.org/Top10/2025/"

print("Loading page...")
driver.get(url)
time.sleep(4)        # Wait for page to fully load (important for JS sites)



# extract top 10 list items using XPath
vulnerabilities = []

items = driver.find_elements(By.XPATH, "//a[contains(text(), 'A0') or contains(text(), 'A10')]")

print(f"Found {len(items)} vulnerabilities.")


for item in items:
    try:
        title = item.text.strip()
        link = item.get_attribute("href")

        vuln_dict = {
            "Vulnerability": title,
            "Link": link
        }

        vulnerabilities.append(vuln_dict)

    except Exception as e:
        print(f"Skipping one item due to error: {e}")
        continue



# Display the scraped vulnerabilities
print("OWASP TOP 10 - SCRAPED DATA")
for vuln in vulnerabilities:
    print(f"Vulnerability: {vuln['Vulnerability']}, Link: {vuln['Link']}")



# convert to DataFrame
df = pd.DataFrame(vulnerabilities)

# Save to CSV
csv_path = 'owasp_top_10.csv'
df.to_csv(csv_path, index=False)
print(f"Data saved to {csv_path}")

driver.quit()