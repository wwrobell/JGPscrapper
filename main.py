from bs4 import BeautifulSoup
import requests
from url_ecg_counter import scrape_url
import time
import csv

def category_calculation(form_2_code):
    cat_sum_ecg = 0
    
    data = {
        'ctl00$ContentPlaceHolder2$ddlKatalogJGP': form_2_code, #form no. 2 selection
        '__EVENTTARGET': second_answer.find('input', {'name': '__EVENTTARGET'}).get('value', ''),
        '__EVENTARGUMENT': second_answer.find('input', {'name': '__EVENTARGUMENT'}).get('value', ''),
        '__LASTFOCUS': second_answer.find('input', {'name': '__LASTFOCUS'}).get('value', ''),
        '__VIEWSTATE': second_answer.find('input', {'name': '__VIEWSTATE'}).get('value', ''),
        '__EVENTVALIDATION': second_answer.find('input', {'name': '__EVENTVALIDATION'}).get('value', ''),
    }
    response = session.post(base_url, data=data)
    
    cat_soup = BeautifulSoup(response.content, 'lxml')
    links = cat_soup.find_all('li')
    for link in links:
        print(link.text)
        cat_sum_ecg += scrape_url((link.find('a').get('href')))

    return cat_sum_ecg



if __name__ == '__main__':
    t = time.time()
    base_url = 'https://prog.nfz.gov.pl/app-jgp/KatalogJGP.aspx'
    ecgs = [];
    years = list(range(2009, 2017)) #2009 - 2016

    with requests.Session() as session:
        session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}

        # parsing parameters
        response = session.get(base_url)
        soup = BeautifulSoup(response.content, 'lxml')

        for year in years:
            annual_ecg_count = 0
            ending = " - Katalog 1a"
            #ending = " - Katalog 1w - Ĺwiadczenia wysokospecjalistyczne"
            
            selection = soup.find('option',text = "Rok " + str(year) + ending)
            if selection:
                form_1_code = selection.get('value')
                
                data = {
                    'ctl00$ContentPlaceHolder2$ddlSymylacjaJGP': form_1_code, #form no. 1 selection
                    '__EVENTTARGET': soup.find('input', {'name': '__EVENTTARGET'}).get('value', ''),
                    '__EVENTARGUMENT': soup.find('input', {'name': '__EVENTARGUMENT'}).get('value', ''),
                    '__LASTFOCUS': soup.find('input', {'name': '__LASTFOCUS'}).get('value', ''),
                    '__VIEWSTATE': soup.find('input', {'name': '__VIEWSTATE'}).get('value', ''),
                    '__EVENTVALIDATION': soup.find('input', {'name': '__EVENTVALIDATION'}).get('value', ''),
                }

                # parsing data
                response = session.post(base_url, data=data)
                second_answer = BeautifulSoup(response.content, 'lxml')

                second_form = second_answer.find('select', id="ContentPlaceHolder2_ddlKatalogJGP")
                options = second_form.find_all('option')

                for option in options[1:]:
                    form_2_code = option.get('value')
                    annual_ecg_count += category_calculation(form_2_code)
            else:
                print('Wrong year')

            ecgs.append([str(year),str(annual_ecg_count)])
            
    csv_out_name = "annual_ECG_1a.csv"
    with open(csv_out_name, "w") as f:
        writer = csv.writer(f)
        writer.writerows(ecgs)
        
    elapsed = time.time() - t

