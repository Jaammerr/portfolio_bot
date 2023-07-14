import json


class Localization:
    def __init__(self):
        self.en_translations = {}
        self.ru_translations = {}
        self.ua_translations = {}
        self.load_translations()

    def load_translations(self):
        with open(f'locales/ru.json', 'r', encoding='utf-8') as file:
            self.ru_translations = json.load(file)

        with open(f'locales/ua.json', 'r', encoding='utf-8') as file:
            self.ua_translations = json.load(file)

        with open(f'locales/en.json', 'r', encoding='utf-8') as file:
            self.en_translations = json.load(file)

    def get_translation(self, key: str, language: str) -> str:
        if language == 'ru':
            return self.ru_translations.get(key)
        elif language == 'ua':
            return self.ua_translations.get(key)
        else:
            return self.en_translations.get(key)
