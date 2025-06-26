from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup

df = pd.read_excel("URLS (2).xlsx", engine='openpyxl')
data = df.values

def setup_driver():
    options = Options()
    options.headless = True  
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_html(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        return driver.page_source
    except Exception as e:
        print(f"Error fetching the URL: {e}")
        return None

def extract_links_with_submenus(driver, url):
    html = fetch_html(driver, url)
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a', href=True)
    links_data = []
    
    for a in a_tags[:45]:  
        link = a['href']
        text = a.get_text(strip=True)
        parent_li = a.find_parent('li')
        submenu_links = []
        if parent_li:
            submenu_ul = parent_li.find('ul')
            if submenu_ul:
                submenu_a_tags = submenu_ul.find_all('a', href=True)
                for submenu_a in submenu_a_tags:
                    submenu_link = submenu_a['href']
                    submenu_text = submenu_a.get_text(strip=True)
                    submenu_links.append(f"{submenu_text} ({submenu_link})")
        links_data.append([text, link] + submenu_links)
    return links_data

def prepare_data_for_excel(links_data):
    max_submenus = max(len(data) - 2 for data in links_data)
    headers = ['Link Text', 'URL'] + [f'Submenu {i+1}' for i in range(max_submenus)]
    prepared_data = []
    for data in links_data:
        prepared_data.append(data + [''] * (max_submenus - len(data) + 2)) 
    return headers, prepared_data

def write_to_excel(headers, data, filename='Extractions_URLS.xlsx'):
    if not data:
        print("No data to write to the Excel file.")
        return
    df = pd.DataFrame(data, columns=headers)
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"Data has been written to {filename}")

def process_urls(urls):
    driver = setup_driver()
    all_data = []
    
    for url in urls:
        print(f"Processing URL: {url}")
        links_data = extract_links_with_submenus(driver, url)
        links_data_with_url = [[url] + row for row in links_data]
        all_data.extend(links_data_with_url)
    
    driver.quit()
    
    headers, data = prepare_data_for_excel(all_data)
    write_to_excel(headers, data)

if __name__ == "__main__":
    urls = [data[j][0] for j in range(len(df))]
    process_urls(urls)
