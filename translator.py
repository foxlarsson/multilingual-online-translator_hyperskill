import sys
import requests
from bs4 import BeautifulSoup
import time
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

args = sys.argv
from_lang_input = args[1]
to_lang_input = args[2]
word_input = args[3]


def choose_language():
    # from_prompt = ''''Hello, you're welcome to the translator. Translator supports:
    #                 1. Arabic
    #                 2. German
    #                 3. English
    #                 4. Spanish
    #                 5. French
    #                 6. Hebrew
    #                 7. Japanese
    #                 8. Dutch
    #                 9. Polish
    #                 10. Portuguese
    #                 11. Romanian
    #                 12. Russian
    #                 13. Turkish
    #                 0. All languages
    #                 Type the number of your language:\n'''
    # # to_prompt = 'Type the number of language you want to translate to or "0" to translate to all languages:\n'
    # # from_code = int(input(from_prompt))
    # # to_code = int(input(to_prompt))
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
        13: 'Turkish',
        0: 'All'
    }
    return from_lang_input, to_lang_input, language_key


def choose_word():
    # word = input('Type the word you want to translate:\n').lower()
    return word_input


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
    translation_list = [word.get_text().strip() for word in translations if word.get_text().strip() != 'Translation']
    examples = soup.select('#examples-content span.text')
    example_list = [phrase.get_text().strip() for phrase in examples]
    return translation_list[:5], example_list[:10]


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


def write_all_to_file(language_list, word):
    with open(f'{word}.txt', 'w') as f:
        for i in range(1, len(language_list)):
            to_lang = language_list[i]
            translations, examples = translate_word(from_lang_input, to_lang, word)
            try:
                f.write(f'{to_lang} Translations:\n{translations[0]}\n\n')
                print(f'{to_lang} Translations:\n{translations[0]}\n\n')
            except IndexError:
                f.write(f'{to_lang} Translations:\nTranslation not available\n\n')
                print(f'{to_lang} Translations:\nTranslation not available\n\n')
            try:
                f.write(f'{to_lang} Examples:\n{examples[0]}\n\n')
                print(f'{to_lang} Examples:\n{examples[1]}\n\n')
            except IndexError:
                f.write(f'{to_lang} Examples:\nExample not available\n\n')
                print(f'{to_lang} Examples:\nExample not available\n\n')
            time.sleep(0.3)


def translate_word(from_language, to_language, word):
    page = get_content(from_language, to_language, word)
    translations, examples = parse_page(page)
    return translations, examples


def main():
    from_language, to_language, language_key = choose_language()
    word = choose_word()
    if to_language == 'all':
        write_all_to_file(language_key, word)
    else:
        translations, examples = translate_word(from_language, to_language, word)
        print_results(translations, examples, to_language)


if len(args) != 4:
    print('The script should be called with 3 arguments: from-language, to-language and word to translate.')
else:
    main()
