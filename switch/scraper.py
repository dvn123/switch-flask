from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_top_5():
    url = "http://francesinhas.com"
    html = urlopen(url)

    soup = BeautifulSoup(html, features="html.parser")
    li = soup.find('div', {'class': 'top-places'})
    children = li.find("ol", recursive=False).findChildren("a", recursive=True)
    res = list()
    for e in children:
        res.append(get_details(e, url))

    return res


def get_details(ele, base_url):
    name = ele.get_text()
    url = base_url + ele['href']
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html.parser")

    address = soup.find('div', {'class': 'address'}).find('p')
    if address is not None:
        address = address.get_text()
        address = ' '.join(filter(lambda x: x not in ['\n', '\r'], address.strip().split()))

    phone_number = soup.find('i', {'class': 'fa fa-phone'})
    if phone_number is not None:
        phone_number = phone_number.next_sibling.next_sibling.get_text()

    email = soup.find('i', {'class': 'fa fa-envelope'})
    if email is not None:
        email = email.next_sibling.next_sibling.get_text()

    link = soup.find('i', {'class': 'fa fa-link'})
    if link is not None:
        link = link.next_sibling.next_sibling.a['href']

    res = {'name': name, 'address': address, 'phone-number': phone_number, 'email': email, 'link': link}
    return res


if __name__ == "__main__":
    get_top_5()
