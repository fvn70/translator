import re
import sys

import requests
from bs4 import BeautifulSoup

def do_request(k_from, k_to, word):
    from_to = langs[k_from].lower() + '-' + langs[k_to].lower()
    url = f"{base}/{from_to}/{word}"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.5'})

    try:
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
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")


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

args = sys.argv
arg_1 = args[1].capitalize()
arg_2 = args[2].capitalize()

try:
    lng_from = langs.index(arg_1)
except:
    print(f"Sorry, the program doesn't support {arg_1}")
try:
    lng_to = -1 if arg_2 == 'All' else langs.index(arg_2)
except:
    print(f"Sorry, the program doesn't support {arg_2}")
    exit()

word = args[3]

fn = f'{word}.txt'

if lng_to < 0:
    for k in range(len(langs)):
        if k != lng_from:
            do_request(lng_from, k, word)
else:
    do_request(lng_from, lng_to, word)

if words:
    write_results()
else:
    print(f"Sorry, unable to find {word}")