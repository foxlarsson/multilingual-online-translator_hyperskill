import requests
from bs4 import BeautifulSoup


def choose_language():
    prompt = 'Type "en" if you want to translate from French to English, or "fr" if you want to translate from ' \
             'English into French:\n'
    language = input(prompt)
    return language


def choose_word():
    word = input('Type the word you want to translate:\n')
    return word


def generate_url_info(target_language):
    if target_language == 'en':
        to_lang = 'english'
        from_lang = 'fren
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


def get_content(target_lang, user_word):
    to_lang, from_lang = generate_url_info(target_lang)
    url = create_url(to_lang, from_lang, user_word)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    headers = {'User-Agent': user_agent}
    response = get_url(url, headers)
    check_connection(response)
    return response


def parse_page(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    translations = soup.find_all('a', class_=lambda value: value and value.startswith("translation"))
    translation_list = [word.get_text().strip() for word in translations]
    examples = soup.select('#examples-content span.text')
    example_list = [phrase.get_text().strip() for phrase in examples]
    return translation_list[3:8], example_list[:10]


def print_results(translation_list, example_list, language):
    if language == 'en':
        print_lang = 'English'
    elif language == 'fr':
        print_lang = 'French'
    print('\nContext examples:')
    print(f'\n{print_lang} Translations:')
    for word in translation_list:
        print(word)
    print(f'\n{print_lang} Examples:')
    pairs = []
    for phrase in example_list:
        if example_list.index(phrase) < len(example_list) - 1 and example_list.index(phrase) % 2 == 0:
            pairs.append((example_list[example_list.index(phrase)], example_list[example_list.index(phrase) + 1]))
    for pair in pairs:
        print(f'{pair[0]}:\n{pair[1]}\n')


def main():
    language = choose_language()
    word = choose_word()
    page = get_content(language, word)
    translations, examples = parse_page(page)
    print_results(translations, examples, language)


main()
