

# # Start browser
# driver = webdriver.Chrome(service=service, options=options)

# # Open a website
# driver.get("https://quotes.toscrape.com/")

# print(driver.title)          # Print page title
# time.sleep(2)                # Wait a bit

# # Close browser
# driver.quit()


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
options.add_argument("--headless")  # Remove this line to see the browser window
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Educational Scraper - Bootcamp Project)")

# Auto-manage driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Target URL from Task 2
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

print("Loading page...")
driver.get(url)
time.sleep(3)        # Wait for page to fully load (important for JS sites)


# Find all search result <li> elements EPLACE WITH THE CLASS FROM TASK 2
search_results = driver.find_elements(By.CLASS_NAME, "cp-search-result-item")

# Extract title and author from each result
books_data = []
for result in search_results:
    title = result.find_element(By.CLASS_NAME, "title-content").text
    author = result.find_element(By.CLASS_NAME, "author-link").text
    books_data.append({"title": title, "author": author})

# Convert to DataFrame
df = pd.DataFrame(books_data)
print(df)