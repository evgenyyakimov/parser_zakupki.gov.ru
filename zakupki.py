import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


CITY = 'Москва'
ITEMS = 50
URL = f'https://zakupki.gov.ru/epz/eruz/search/results.html?&address={CITY}&recordsPerPage={ITEMS}'


def extract_max_page():
    zakupki_request = requests.get(URL, headers={'User-Agent': UserAgent().chrome})
    zakupki_soup = BeautifulSoup(zakupki_request.text, 'html.parser')
    pages = []
    paginator = zakupki_soup.find_all("a", class_='page__link')
    for page in paginator:
        pages.append(int(page.find("span", class_='link-text').text))
    return pages[-1]

def extract_data(html):
    try:
        urls = []
        e_mail = []
        telefon = []
        address = []
        fio = []
        e_dol = []
        d_inn = []
        title = html.find('div', class_='registry-entry__body-href').find('a').text
        title = title.strip()
        link = html.find('a')['href']
        urls.append('http://zakupki.gov.ru' + link)
        number = html.find('div', class_='registry-entry__header').find('a').text
        number = number.strip()
        number = number.partition(' ')[2]
        inn = html.find('div', class_='registry-entry__body-value').text
        inn = inn.strip()
        kpp = html.find_all('div', class_='registry-entry__body-value')[1].text
        kpp = kpp.strip()
        ogrn = html.find_all('div', class_='registry-entry__body-value')[2].text
        ogrn = ogrn.strip()
        for url in urls:
            result = requests.get(url, headers={'User-Agent': UserAgent().chrome})
            soup = BeautifulSoup(result.text, 'html.parser')
            email = soup.find_all('div', class_='row')[8].find_all('section', class_='section')[1].find('span', class_='section__info').text
            e_mail.append(email)
            tel = soup.find_all('div', class_='row')[8].find_all('section', class_='section')[2].find('span', class_='section__info').text
            telefon.append(tel)
            add = soup.find_all('div', class_='row')[8].find_all('section', class_='section')[0].find('span', class_='section__info').text
            address.append(add)
            name = soup.find_all('div', class_='row')[7].find('td', class_='tableBlock__col').text
            fio.append(name)
            dol = soup.find_all('div', class_='row')[7].find_all('td', class_='tableBlock__col')[1].text
            e_dol.append(dol)
            dinn = soup.find_all('div', class_='row')[7].find_all('td', class_='tableBlock__col')[2].text
            d_inn.append(dinn)
    except IOError:
        print('Error')
        continue
    return {
            'title': title, 'number': number, 'inn': inn, 'kpp': kpp, 
            'link': 'zakupki.gov.ru' + link, 'telefon': ''.join(telefon), 
            'email': ''.join(e_mail), 'address': ''.join(address), 'FIO': ''.join(fio),
            'Dolzhnost': ''.join(e_dol), 'Dir inn': ''.join(d_inn)
            }

def extract_org(last_page):
    orgs = []
    for page in range(1, last_page + 1):
        print(f'Парсинг страницы {page}')
        result = requests.get(f'{URL}&pageNumber={page}', headers={'User-Agent': UserAgent().chrome})
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', class_='col-8 pr-0 mr-21px')
        for result in results:
            org = extract_data(result)
            orgs.append(org)
    return orgs
