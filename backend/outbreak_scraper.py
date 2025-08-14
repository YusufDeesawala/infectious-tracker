import requests
from bs4 import BeautifulSoup
import json
import time

def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error if request fails
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_cdc_outbreaks():
    url = "https://www.cdc.gov/outbreaks/index.html"
    soup = get_soup(url)
    if not soup:
        return []
    outbreaks = []
    for h2 in soup.find_all('h2'):
        section = h2.text.strip()
        if 'outbreak' in section.lower():  # Focus on outbreak sections
            table = h2.find_next('table')
            if table:
                headers = [th.text.strip() for th in table.find('thead').find_all('th')]
                for row in table.find('tbody').find_all('tr'):
                    cells = row.find_all('td')
                    data = [cell.text.strip() for cell in cells]
                    outbreak = dict(zip(headers, data))
                    outbreak['section'] = section
                    outbreak['source'] = 'CDC'
                    a = cells[0].find('a') if cells else None
                    if a:
                        detail_url = a['href']
                        if not detail_url.startswith('http'):
                            detail_url = "https://www.cdc.gov" + detail_url
                        outbreak['link'] = detail_url
                        time.sleep(1)  # Rate limit
                        detail_soup = get_soup(detail_url)
                        if detail_soup:
                            content = detail_soup.find('div', id='content') or detail_soup.find('main')
                            if content:
                                full_text = '\n'.join([p.text.strip() for p in content.find_all('p')])
                                outbreak['full_text'] = full_text
                    outbreaks.append(outbreak)
    return outbreaks

def scrape_cdc_travel_notices():
    url = "https://wwwnc.cdc.gov/travel/notices"
    soup = get_soup(url)
    if not soup:
        return []
    notices = []
    for h3 in soup.find_all('h3'):
        level = h3.text.strip()
        ul = h3.find_next('ul')
        if ul:
            for li in ul.find_all('li'):
                a = li.find('a')
                if a:
                    title = a.text.strip()
                    link = a['href']
                    if not link.startswith('http'):
                        link = "https://wwwnc.cdc.gov" + link
                    notice = {
                        'title': title,
                        'level': level,
                        'link': link,
                        'section': 'International Travel Health Notices',
                        'source': 'CDC'
                    }
                    time.sleep(1)  # Rate limit
                    detail_soup = get_soup(link)
                    if detail_soup:
                        content = detail_soup.find('div', id='content')
                        if content:
                            full_text = '\n'.join([p.text.strip() for p in content.find_all('p')])
                            notice['full_text'] = full_text
                    notices.append(notice)
    return notices

def scrape_who_dons():
    base_url = "https://www.who.int/emergencies/disease-outbreak-news"
    outbreaks = []
    page = 1
    while True:
        url = base_url if page == 1 else f"{base_url}?page={page}"
        soup = get_soup(url)
        if not soup:
            break
        items = soup.find_all('article', class_='teaser')
        if not items:
            break
        for item in items:
            title_tag = item.find('h3', class_='teaser__title')
            if title_tag:
                a = title_tag.find('a')
                if a:
                    title = a.text.strip()
                    link = a['href']
                    if link.startswith('/'):
                        link = 'https://www.who.int' + link
                    date = item.find('span', class_='timestamp').text.strip() if item.find('span', class_='timestamp') else ''
                    summary = item.find('p', class_='teaser__body').text.strip() if item.find('p', class_='teaser__body') else ''
                    outbreak = {
                        'title': title,
                        'date': date,
                        'summary': summary,
                        'link': link,
                        'source': 'WHO'
                    }
                    time.sleep(1)  # Rate limit
                    detail_soup = get_soup(link)
                    if detail_soup:
                        content = detail_soup.find('div', class_='sf-prose')
                        if content:
                            full_text = '\n'.join([p.text.strip() for p in content.find_all('p')])
                            outbreak['full_text'] = full_text
                    outbreaks.append(outbreak)
        page += 1
    return outbreaks

# Main execution
cdc_outbreaks = scrape_cdc_outbreaks()
cdc_travel = scrape_cdc_travel_notices()
who_dons = scrape_who_dons()

all_outbreaks = cdc_outbreaks + cdc_travel + who_dons

with open('all_outbreaks.json', 'w', encoding='utf-8') as f:
    json.dump(all_outbreaks, f, indent=4, ensure_ascii=False)

print("Scraping completed. Data saved to all_outbreaks.json")