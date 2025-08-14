from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time
from webdriver_manager.chrome import ChromeDriverManager

# URL for Google News Health section
url = 'https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen'

# Set up Selenium WebDriver with automatic ChromeDriver management
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (optional, comment out to see browser)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Load the page
    driver.get(url)

    # Wait for articles to load (adjust timeout as needed)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'article'))
    )

    # Scroll to ensure more content loads (optional, adjust as needed)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for dynamic content to load

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract articles (using more generic selectors)
    articles = soup.find_all('article')

    if not articles:
        print("No articles found. Check the page structure or selectors.")
        driver.quit()
        exit()

    news_data = []
    for article in articles:
        # Extract title (look for h3 or h4 tags commonly used for headlines)
        title_elem = article.find(['h3', 'h4'])
        title = title_elem.text.strip() if title_elem else 'N/A'

        # Extract source (often in a div or span with specific classes)
        source_elem = article.find('div', class_=lambda x: x and 'sourcename' in x.lower()) or article.find('a', class_=lambda x: x and 'source' in x.lower())
        source = source_elem.text.strip() if source_elem else 'N/A'

        # Extract datetime (look for time tag)
        datetime_elem = article.find('time')
        datetime = datetime_elem.text.strip() if datetime_elem else 'N/A'

        # Extract link (look for anchor tags with href)
        link_elem = article.find('a', href=True)
        link = 'https://news.google.com' + link_elem['href'][1:] if link_elem and link_elem['href'].startswith('./') else link_elem['href'] if link_elem else 'N/A'

        if title != 'N/A' or source != 'N/A' or datetime != 'N/A' or link != 'N/A':
            news_data.append({
                'Title': title,
                'Source': source,
                'Datetime': datetime,
                'Link': link
            })

    # Save to CSV file
    if news_data:
        with open('google_health_news.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Source', 'Datetime', 'Link'])
            writer.writeheader()
            writer.writerows(news_data)
        print(f"Scraped {len(news_data)} articles and saved to google_health_news.csv")
    else:
        print("No valid news data scraped. Inspect the page source or selectors.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the driver
    driver.quit()