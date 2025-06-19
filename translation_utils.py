# translation_utils.py

from deep_translator import GoogleTranslator

def translate_to_urdu(text):
    try:
        translated = GoogleTranslator(source='auto', target='ur').translate(text)
        return translated
    except Exception as e:
        return f"Translation failed: {str(e)}"
