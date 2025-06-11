from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver (update chromedriver path if needed)
driver = webdriver.Chrome(options=chrome_options)

# List to store results
scraped_data = []
# Starting URL
current_url = "https://chaidocs.vercel.app/youtube/getting-started/"


# Extract text while preserving some structure
def extract_structured_text(element):
    text_parts = []
    
    for child in element.children:
        if child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text_parts.append(f"\n{child.get_text()}\n{'-'*len(child.get_text())}")
        elif child.name == 'p':
            text_parts.append(f"\n{child.get_text()}")
        elif child.name == 'li':
            text_parts.append(f"• {child.get_text()}")
        elif child.name in ['div', 'span', 'a']:
            text_parts.append(child.get_text())
        elif child.name is None:  # Text node
            stripped = child.strip()
            if stripped:
                text_parts.append(stripped)
    
    return ' '.join(text_parts).replace('  ', ' ')

 

try:
    while current_url:
        print(f"Processing: {current_url}")
        
        # Load page with Selenium
        driver.get(current_url)
        time.sleep(2)  # Allow page to load
        
        # Get page source and parse with Beautiful Soup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        main_content = soup.find('main') # Find the main content area
        # Store in dictionary

        heading = main_content.find('h1').get_text()
        scraped_data.append({
            'heading': heading,
            'url': current_url,
            'content': extract_structured_text(main_content)
        })
        
        # Find next page link
        next_link = soup.find('a', {'rel': 'next', 'class': 'astro-apwlwm3s'})
        
        if next_link and (href := next_link.get('href')):
            current_url = urljoin(current_url, href)
        else:
            print("No more pages found")
            current_url = None
except Exception as e:
    with open("scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(
            scraped_data,
            f,
            ensure_ascii=False,
            indent=2
        )
# Print results
print("\nScraped Data Summary:")
for entry in scraped_data:
    print(f"- {entry['url']}: {len(entry['content'])} characters")

# Example: Access content for first URL
# print(scraped_data[0]['content'][:500])
# Example: Access content for first URL
# print(scraped_data["https://chaidocs.vercel.app/youtube/getting-started/"][:500])