import re
import sys

import requests
from bs4 import BeautifulSoup

def do_request(p_from, p_to, word):
    from_to = langs[p_from].lower() + '-' + langs[p_to].lower()
    url = f"{base}/{from_to}/{word}"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.5'})

    try:
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
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")

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


fn = word + '.txt'
if lng_to < 0:
    for k in range(13):
        if k != lng_from:
            do_request(lng_from, k, word)
else:
    do_request(lng_from, lng_to, word)

if words:
    write_results()
else:
    print(f"Sorry, unable to find {word}")
