import requests
from bs4 import BeautifulSoup


def choose_action():
    prompt = 'Type "en" if you want to translate from French to English, or "fr" if you want to translate from ' \
             'English into French:\n'
    language = input(prompt)
    word = input('Type the word you want to translate:\n')
    print(f'You chose "{language}" as a language to translate "{word}".')
    return language, word


def generate_url_info(target_language):
    if target_language == 'en':
        to_lang = 'english'
        from_lang = 'french'
    else:
        to_lang = 'french'
        from_lang = 'english'
    return to_lang, from_lang


def create_url(to_lang, from_lang, word):
    url = f'https://context.reverso.net/translation/{from_lang}-{to_lang}/{word}'
    return url


def get_url(gen_url, header):
    return requests.get(gen_url, headers=header)


def check_connection(url):
    if url.status_code == 200:
        print('200 OK')


target_lang, user_word = choose_action()
to_lang, from_lang = generate_url_info(target_lang)
url = create_url(to_lang, from_lang, user_word)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
headers = {'User-Agent': user_agent}
response = get_url(url, headers)

soup = BeautifulSoup(response.content, 'html.parser')

translations = soup.find_all('a', class_=lambda value: value and value.startswith("translation"))
translation_list = [word.get_text().strip() for word in translations]
examples = soup.select('#examples-content span.text')
example_list = [phrase.get_text().strip() for phrase in examples]

check_connection(response)
print(translation_list[2:])
print(example_list[:-2])
