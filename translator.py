import requests
from bs4 import BeautifulSoup


def choose_language():
    from_prompt = ''''Hello, you're welcome to the translator. Translator supports: 
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
                    13. Turkish
                    Type the number of your language:\n'''
    to_prompt = 'Type the number of language you want to translate to:\n'
    from_code = int(input(from_prompt))
    to_code = int(input(to_prompt))
    language_key = {
        1: 'Arabic',
        2: 'German',
        3: 'English',
        4: 'Spanish',
        5: 'French',
        6: 'Hebrew',
        7: 'Japanese',
        8: 'Dutch',
        9: 'Polish',
        10: 'Portuguese',
        11: 'Romanian',
        12: 'Russian',
        13: 'Turkish'
    }
    from_language = language_key[from_code]
    to_language = language_key[to_code]
    return from_language, to_language


def choose_word():
    word = input('Type the word you want to translate:\n').lower()
    return word


def create_url(from_lang, to_lang, word):
    url = f'https://context.reverso.net/translation/{from_lang.lower()}-{to_lang.lower()}/{word}'
    return url


def get_url(gen_url, header):
    return requests.get(gen_url, headers=header)


def check_connection(url):
    if url.status_code == 200:
        print('200 OK')


def get_content(from_lang, to_lang, user_word):
    url = create_url(from_lang, to_lang, user_word)
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


def print_results(translation_list, example_list, to_lang):
    print('\nContext examples:')
    print(f'\n{to_lang} Translations:')
    for word in translation_list:
        print(word)
    print(f'\n{to_lang} Examples:')
    pairs = []
    for phrase in example_list:
        if example_list.index(phrase) < len(example_list) - 1 and example_list.index(phrase) % 2 == 0:
            pairs.append((example_list[example_list.index(phrase)], example_list[example_list.index(phrase) + 1]))
    for pair in pairs:
        print(f'{pair[0]}:\n{pair[1]}\n')


def main():
    from_language, to_language = choose_language()
    word = choose_word()
    page = get_content(from_language, to_language, word)
    translations, examples = parse_page(page)
    print_results(translations, examples, to_language)


main()
