import re
import sys

import requests
from bs4 import BeautifulSoup

def do_request(p_from, p_to, word):
    from_to = langs[p_from].lower() + '-' + langs[p_to].lower()
    url = f"{base}/{from_to}/{word}"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.5'})

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        tr_content = soup.find('div', {'id':"translations-content"})
        if tr_content:
            lst = tr_content.find_all('a', class_=re.compile('translation.*'))
            if lst:
                words[p_to] = lst[0].text.strip()

                ex_content = soup.find('section', {'id':"examples-content"})
                lst = ex_content.find_all('span', {'class':'text'})
                examples[p_to] = [lst[0].text.strip(), lst[1].text.strip()]

                print_result(p_to)
    else:
        print(r.status_code)

def print_result(k):
    print(f"\n{langs[k]} Translations:")
    print(words[k])
    print(f"\n{langs[k]} Example:")
    print(examples[k][0])
    print(examples[k][1])

def write_results():
    with open(fn, 'wb') as file:
        for k in words:
            file.write(bytes(f"\n{langs[k]} Translations:\n", encoding='utf-8'))
            file.write(bytes(f"{words[k]}\n", encoding='utf-8'))
            file.write(bytes(f"\n{langs[k]} Example:\n", encoding='utf-8'))
            file.write(bytes(f"{examples[k][0]}\n", encoding='utf-8'))
            file.write(bytes(f"{examples[k][1]}\n", encoding='utf-8'))


base = "https://context.reverso.net/translation"
lngs = {'fr': 'French', 'en': 'English'}
langs = ['Arabic', 'German', 'English', 'Spanish','French', 'Hebrew', 'Japanese',
         'Dutch','Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
word = 'hello'
words = {}
examples = {}

args = sys.argv

print("Hello, you're welcome to the translator. Translator supports: ")
print('''
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish''')

lng_from = int(input('Type the number of your language:\n')) - 1
lng_to = int(input('Type the number of a language you want to translate to or "0" to translate to all languages:\n')) - 1
word = input('Type the word you want to translate:\n')

fn = word + '.txt'
if lng_to < 0:
    for k in range(13):
        if k != lng_from:
            do_request(lng_from, k, word)
else:
    do_request(lng_from, lng_to, word)
write_results()