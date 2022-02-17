import re

import requests
from bs4 import BeautifulSoup

def do_request(k_from, k_to, word):
    from_to = langs[k_from].lower() + '-' + langs[k_to].lower()
    url = f"{base}/{from_to}/{word}"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.5'})

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        tr_content = soup.find('div', {'id':"translations-content"})
        if tr_content:
            lst = tr_content.find_all('a', class_=re.compile('translation.*'))
            if lst:
                words[k_to] = lst[0].text.strip()

                ex_content = soup.find('section', {'id':"examples-content"})
                lst = ex_content.find_all('span', {'class':'text'})
                examples[k_to] = [lst[0].text.strip(), lst[1].text.strip()]
            print_result(k_to)
    else:
        print(r.status_code)


def print_result(k):
    print(f"\n{langs[k]} Translations:\n{words[k]}")
    print(f"\n{langs[k]} Examples:\n{examples[k][0]}\n{examples[k][1]}")


def write_results():
    with open(fn, 'wb') as file:
        for k in words:
            file.write(bytes(f"\n{langs[k]} Translations:\n{words[k]}\n", encoding='utf-8'))
            file.write(bytes(f"\n{langs[k]} Examples:\n{examples[k][0]}\n{examples[k][1]}\n", encoding='utf-8'))


base = "https://context.reverso.net/translation"
langs = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
         'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
words = {}
examples = {}

print("Hello, you're welcome to the translator. Translator supports:")
for i in range(len(langs)):
    print(f"{i + 1}. {langs[i]}")
lng_from = int(input('Type the number of your language:\n')) - 1
lng_to = int(input('Type the number of language you want to translate to:\n')) - 1
word = input('Type the word you want to translate:\n')
fn = f'{word}.txt'

if lng_to < 0:
    for k in range(len(langs)):
        if k != lng_from:
            do_request(lng_from, k, word)
else:
    do_request(lng_from, lng_to, word)
write_results()