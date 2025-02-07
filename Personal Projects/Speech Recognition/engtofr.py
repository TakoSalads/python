import speech_recognition as sr
from googletrans import Translator
import language_tool_python

# Initialize global objects for efficiency
translator = Translator()
english_tool = language_tool_python.LanguageTool('en-US')
french_tool = language_tool_python.LanguageTool('fr-FR')

def recognize_speech(language):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Please speak in {language}...")
        recognizer.adjust_for_ambient_noise(source)  # Improve accuracy
        try:
            if language == "fr":
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)  # Increased for French
            else:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return None

    try:
        recognized_text = recognizer.recognize_google(audio, language=language)
        print(f"\nRecognized {language} Text: {recognized_text}\n")
        return recognized_text
    except sr.UnknownValueError:
        print("Could not understand the audio. Please try again.")
    except sr.RequestError:
        print("Error connecting to Google Speech Recognition service.")
    
    return None

def translate_text(text, src_lang, dest_lang):
    try:
        translation = translator.translate(text, src=src_lang, dest=dest_lang)
        print(f"Translated {dest_lang} Text: {translation.text}\n")
        return translation.text
    except Exception as e:
        print(f"Translation Error: {e}")
        return text  # Fallback to original text

def correct_grammar(text, tool):
    try:
        return tool.correct(text)
    except Exception as e:
        print(f"Grammar Correction Error: {e}")
        return text  # Fallback to uncorrected text

def main():
    # Let the user choose the input language
    print("Welcome to the Speech Translator!")
    print("Choose the input language:")
    print("1. English")
    print("2. French")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        input_lang = "en"
        output_lang = "fr"
        grammar_tool = english_tool
        print("You have chosen English as the input language. Translations will be to French.")
    elif choice == "2":
        input_lang = "fr"
        output_lang = "en"
        grammar_tool = french_tool
        print("You have chosen French as the input language. Translations will be to English.")
    else:
        print("Invalid choice. Exiting the program.")
        return

    while True:
        # Recognize speech in the chosen input language
        recognized_text = recognize_speech(input_lang)
        if not recognized_text:
            continue  # Skip to the next iteration if no speech is detected
        
        # Grammar check
        corrected_text = correct_grammar(recognized_text, grammar_tool)
        print(f"Corrected {input_lang} Text: {corrected_text}\n")

        # Translate to the target language
        translated_text = translate_text(corrected_text, input_lang, output_lang)

        # Correct grammar in the translated text (optional)
        if output_lang == "en":
            corrected_translation = correct_grammar(translated_text, english_tool)
        elif output_lang == "fr":
            corrected_translation = correct_grammar(translated_text, french_tool)
        print(f"Corrected {output_lang} Text: {corrected_translation}\n")

        # Ask the user if they want to continue
        user_input = input("Do you want to translate another phrase? (yes/no): ").strip().lower()
        if user_input != 'yes':
            print("Exiting the translation loop. Goodbye!")
            break

if __name__ == "__main__":
    main()
