from bs4 import BeautifulSoup
import requests
import re

def scrape_url(url):
    wanted_icds = re.compile('89.502|89.5[1-7]|89.5[1-7]\d+|75.32|89.43')
    quantity_sum = 0
    response = requests.get(url)
    if response.status_code != 200:
        print('Warning! The request hasn\'t succeeded.')
    
    soup = BeautifulSoup(response.content, 'lxml')
    title = soup.find_all('div',text = re.compile("Procedury ICD 9"))
    if title:
        table_icd = title[-1].findNext('table')
        tr_all = table_icd.find_all('tr')

        for tr in tr_all:
            icd_num = tr.find('td', class_="lewa")
            if icd_num:
                if wanted_icds.findall(icd_num.text): #find icds which fit to pattern
                    quantity = tr.find('td', class_="prawa") #get number of hospitalizations
                    quantity_sum += int(quantity.text)
                    print (icd_num.contents[0],quantity.contents[0])
    return quantity_sum

if __name__ == '__main__':
    url = 'https://prog.nfz.gov.pl/app-jgp/Grupa.aspx?id=KAd2LOnzgjU%3d'
    output = scrape_url(url)
