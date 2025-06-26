import requests
from bs4 import BeautifulSoup
import pandas as pd
df=pd.read_excel("URLS.xlsx",engine='openpyxl')
data=df.values
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
def extract_links_with_submenus(html):
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a', href=True)
    links_data = []
    
    for a in a_tags[:35]:  
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
    all_data = []
    
    for url in urls:
        print(f"Processing URL: {url}")
        html = fetch_html(url)
        if html:
            links_data = extract_links_with_submenus(html)
            links_data_with_url = [[url] + row for row in links_data]
            all_data.extend(links_data_with_url)
    headers, data = prepare_data_for_excel(all_data)
    write_to_excel(headers, data)
if __name__ == "__main__":
    urls=[]
    for j in range(0,len(df)):
        y=data[j][0]
        urls.append(y)
    process_urls(urls)
