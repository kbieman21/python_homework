# Task 1: Review robots.txt to Ensure Policy Compliance

# I visited https://durhamcountylibrary.org/robots.txt and reviewed the policy.
# Key Findings:
# The robots.txt file is relatively permissive.
# The only restriction for general crawlers (User-agent: *) is:
# Disallow: /staff/


# Task 2: Understanding HTML and the DOM for the Durham Library Site

# <li class="row cp-search-result-item fade-enter-done">
# <span aria-hidden="true" class="title-content">Animal Farm</span>
# <span class="cp-author-link"><span><a target="_parent" rel="noopener noreferrer" class="author-link" data-key="author-link" href="/v2/search?origin=core-catalog-explore&amp;query=Orwell%2C%20George&amp;searchType=author">Orwell, George</a></span></span>
# <div class="format">eBook, 2025 — Spanish</div>


# Task 3: Write a Program to Extract this Data

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup browser options
options = Options()
options.add_argument("--headless")  # Remove this line to see the browser window for debugging
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Educational Scraper - Bootcamp Project)")

# Auto-manage driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Target URL from Task 2
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

print("Loading page...")
driver.get(url)
time.sleep(4)        # Wait for page to fully load (important for JS sites)


# Find all search result <li> elements REPLACE WITH THE CLASS FROM TASK 2
search_results = driver.find_elements(By.CLASS_NAME, "cp-search-result-item")

print(f"Found {len(search_results)} book results.")

# Extract title, author, and format of the year from each result
books_data = []

for result in search_results:
    try:
        # Title
        title = result.find_element(By.CLASS_NAME, "title-content").text.strip()

        # Author(s) - Handling multiple authors
        author_elements = result.find_elements(By.CLASS_NAME, "author-link")
        authors = [author.text.strip() for author in author_elements if author.text.strip()]
        author_str = "; ".join(authors) if authors else "No Author"

        # format
        format_info = result.find_element(By.CLASS_NAME, "format").text.strip() if result.find_elements(By.CLASS_NAME, "format") else "No Format"

        book = {
            "Title": title,
            "Author": author_str,
            "Format": format_info
        }

        books_data.append(book)

    except Exception as e:
        print(f"Skipping one item due to error: {e}")
        continue

# Convert to DataFrame
df = pd.DataFrame(books_data)
#print("SCRAPED BOOKS FROM DURHAM COUNTY LIBRARY")
#print(df)



# Task 4: Write out the Data
import json
import os


# Create assignment8 folder if it doesn't exist
#os.makedirs('assignment8', exist_ok=True)

# Save to CSV
csv_path = 'get_books.csv'
df.to_csv(csv_path, index=False)
print(f"Data saved to {csv_path}")

# Save to JSON
json_path = 'get_books.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(books_data, f, ensure_ascii=False, indent=4)
print(f"Data saved to {json_path}")

print("SCRAPED BOOKS FROM DURHAM COUNTY LIBRARY AFTER SAVING TO FILES")
print(df)

# Close browser
#driver.quit()