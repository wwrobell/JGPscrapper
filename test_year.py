from url_ecg_counter import scrape_url
from bs4 import BeautifulSoup
import requests

def category_calculation(href, year):
    cat_sum_ecg = 0
    body = "https://prog.nfz.gov.pl/app-jgp/"
    response = session.get(body + href)  
    cat_soup = BeautifulSoup(response.content, 'lxml')
    year_links = cat_soup.find_all('a',text = str(year) +" r.")
    if year_links:
        url = year_links[0].get('href')
        cat_sum_ecg = scrape_url(url)
    
    return cat_sum_ecg



if __name__ == '__main__':
    base_url = 'https://prog.nfz.gov.pl/app-jgp/AnalizaPrzekrojowa.aspx'
    year = 2015
    total_ecg = 0;
    
    with requests.Session() as session:
        session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}

        # parsing parameters
        response = session.get(base_url)
        soup = BeautifulSoup(response.content, 'lxml')
        all_links = soup.find_all('a')
        for link in all_links[6:]:
            href = link.get('href')
            if href:
                print(link.text)
                total_ecg+=category_calculation(href, year)
        
    print(str(total_ecg))
