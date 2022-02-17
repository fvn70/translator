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
    print(f"\n{langs[k]} Translations:")
    for word in words[:5]:
        print(word)
    print(f"\n{langs[k]} Examples:")
    for i in range(0, 10, 2):
        print(examples[i])
        print(examples[i + 1])
        print()


base = "https://context.reverso.net/translation"
langs = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
         'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
words = []
examples = []

print("Hello, you're welcome to the translator. Translator supports:")
for i in range(len(langs)):
    print(f"{i + 1}. {langs[i]}")
lng_from = input('Type the number of your language:\n')
lng_to = input('Type the number of language you want to translate to:\n')
word = input('Type the word you want to translate:\n')

do_request(int(lng_from) - 1, int(lng_to) - 1, word)
