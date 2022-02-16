import re

import requests
from bs4 import BeautifulSoup

def do_request(k_from, k_to, word):
    from_to = lngs[k_from].lower() + '-' + lngs[k_to].lower()
    url = f"{base}/{from_to}/{word}"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.5'})

    if r.status_code == 200:
        print('200 OK')
        soup = BeautifulSoup(r.content, 'html.parser')
        tr_content = soup.find('div', {'id':"translations-content"})
        if tr_content:
            lst = tr_content.find_all('a', class_=re.compile('translation.*'))
            if lst:
                for l in lst:
                    words.append(l.text.strip())

                ex_content = soup.find('section', {'id':"examples-content"})
                lst = ex_content.find_all('span', {'class':'text'})
                for l in lst:
                    examples.append(l.text.strip())

                print_result(k_to)
    else:
        print(r.status_code)


def print_result(k):
    print(f"\nTranslations")
    print(words)
    print(examples)


base = "https://context.reverso.net/translation"
lngs = {'fr': 'French', 'en': 'English'}
words = []
examples = []

lng_to = input('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:\n')
lng_from = 'fr' if lng_to == 'en' else 'en'
word = input('Type the word you want to translate:\n')
print(f'You chose "{lng_to}" as the language to translate "{word}" to.')

do_request(lng_from, lng_to, word)
