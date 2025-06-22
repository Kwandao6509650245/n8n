import asyncio
from googletrans import Translator

# Define the async translation function
async def translate_text_googletrans(text, dest_language='en', src_language='auto'):
    try:
        translator = Translator()
        # AWAIT the translate method
        translated = await translator.translate(text, dest=dest_language, src=src_language)
        return translated.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

# Create an async main function to orchestrate your script
async def main():
    text_to_translate_thai = "ขอเปลี่ยนรหัสผ่าน"
    print(f"Original Thai text: {text_to_translate_thai}")

    # Call the async translation function using await
    translated_thai_to_english = await translate_text_googletrans(text_to_translate_thai, dest_language='en')

    if translated_thai_to_english:
        print(f"Translated to English: {translated_thai_to_english}")
    else:
        print("Translation failed.")

# This is the single entry point to run your async code
if __name__ == "__main__":
    asyncio.run(main())