from deep_translator import GoogleTranslator



def translate_text(text: str, language: str) -> str:
    try:
        translated = GoogleTranslator(source='ru', target='uk' if language == 'ua' else language).translate(text)
        return translated

    except Exception as e:
        print(f'Error while translating text to {language}: {e}')
        return text
