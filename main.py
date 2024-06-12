from flask import Flask, render_template_string, request, redirect, url_for ,session
from bs4 import BeautifulSoup
import speech_recognition as sr
from translate import Translator as MicrosoftTranslator
import requests

a = 0
app = Flask(__name__)
app.secret_key = "abcdef"

# HTML templates
html_template1 = """
<!DOCTYPE html>
<head>
    <title>
        feedback form
    </title>
    <link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
</head>
<body>
    <div class="container">
        <div class="topic-bg">
        <div><h1 class="topic">Flipkart survey form</h1></div>
        </div>
        <div class="cont-bg">
            <div class="cont" lang="{{ lang_code }}">1.Have you used our app?</div>
            <div class="ipt"><input type="text" class="txt" id="textbox1" name="textbox1" value="{{ default_value }}">
            <form method="post" action='/'>
            <input type="image" src="{{ url_for('static', filename='micro.svg') }}" alt="Submit" id="imageBtn">
            </form>
            </div>
            <div class="bttn"><a href="{{ url_for('app2_index') }}"> <button class="btn"lang="{{ lang_code }}">Next</button></a></div>
        </div>
    </div>
    <div>
            Language:
            <a href="/lang/en">English</a> |
            <a href="/lang/fr">French</a> |
            <a href="/lang/es">Spanish</a> |
            <a href="/lang/ta">Tamil</a>
          </div>
</body>
</html>

"""

html_template2 = """
<!DOCTYPE html>
<head>
    <title>
        feedback form
    </title>
    <link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
</head>
<body>
    <div class="container">
        <div class="topic-bg">
        <div><h1 class="topic">Flipkart survey form</h1></div>
        </div>
        <div class="cont-bg">
            <div class="cont" lang="{{ lang_code }}">2. Tell us the phone model or android version you are using</div>
            <div class="ipt"><input type="text" class="txt" id="textbox1" name="textbox1" value="{{ default_value }}">
            <form method="post" action="/">
            <input type="image" src="{{ url_for('static', filename='micro.svg') }}" alt="Submit" id="imageBtn">
            </form>
            </div>
            <div class="bttn"><a href="{{ url_for('app2_index') }}"> <button class="btn"lang="{{ lang_code }}">Next</button></a></div>
        </div>
    </div>
    <div>
            Language:
            <a href="/lang/en">English</a> |
            <a href="/lang/fr">French</a> |
            <a href="/lang/es">Spanish</a> |
            <a href="/lang/ta">Tamil</a>
          </div>
</body>
</html>

"""

html_template3 = """
<!DOCTYPE html>
<head>
    <title>
        feedback form
    </title>
    <link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
</head>
<body>
    <div class="container">
        <div class="topic-bg">
        <div><h1 class="topic">Flipkart survey form</h1></div>
        </div>
        <div class="cont-bg">
            <div class="cont" lang="{{ lang_code }}">3. Do you have the app currently installed</div>
            <div class="ipt"><input type="text" class="txt"><input type="image" src="{{ url_for('static', filename='micro.svg') }}" alt="Submit" id="imageBtn"></div>
            <div class="bttn"><a href="{{ url_for('app3_index') }}"> <button class="btn"lang="{{ lang_code }}">Next</button></a></div>
        </div>
    </div>
    <div>
            Language:
            <a href="/lang/en">English</a> |
            <a href="/lang/fr">French</a> |
            <a href="/lang/es">Spanish</a> |
            <a href="/lang/ta">Tamil</a>
          </div>
</body>
</html>

"""



def recognize_and_translate_to_english():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        recognized_text = recognizer.recognize_google(audio, language='ta-IN')
        if recognized_text:
            print('Recognized Text (Tamil):', recognized_text)
            return recognized_text
        else:
            print("Speech recognition did not capture any text.")
            return None

    except sr.WaitTimeoutError:
        print("Speech recognition timed out. No speech detected.")
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def translate_to_english(text):
    if text:
        translator = MicrosoftTranslator(from_lang='ta', to_lang='en')
        translated_text = translator.translate(text)

        # Check if the translation is meaningful
        if not translated_text:
            translated_text = "Translation not available or meaningful in English."

        print('Translated Text (Tamil to English):', translated_text)
        return translated_text
    return None


def translate_template(template, target_lang):
    soup = BeautifulSoup(template, 'html.parser')
    translator = MicrosoftTranslator(from_lang='en', to_lang=target_lang)

    for tag in soup.find_all(lambda tag: tag.has_attr("lang")):
        original_text = tag.get_text(strip=True)
        if original_text:
            translated_text = translator.translate(original_text)
            if translated_text:
                tag.string.replace_with(translated_text)

    translated_template = str(soup)
    return translated_template


def send_translated_text_to_php(translated_text):
    # Replace 'http://your_domain/insert_data.php' with the actual URL of your PHP script
    url = 'http://localhost/voc/insert_data.php'
    data = {'translated_text': translated_text}

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Data sent successfully to PHP script.")
    else:
        print("Error sending data to PHP script.")

@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if 'lang_code' is already stored in the session
    if 'lang_code' in session:
        lang_code = session['lang_code']
    else:
        lang_code = request.accept_languages.best_match(['en', 'fr', 'es', 'ta'])

    if request.method == 'POST':
        recognized_text = recognize_and_translate_to_english()
        translated_text = translate_to_english(recognized_text)
        page_num = request.form.get('page_num', '1')
        send_translated_text_to_php(translated_text)
    else:
        recognized_text = None
    return render_template_string(html_template1, message=recognized_text, default_value=recognized_text)




@app.route('/lang/<lang_code>')
def change_language(lang_code):
    # Store the language preference in session
    session['lang_code'] = lang_code
    translated_template1 = translate_template(html_template1, lang_code)
    translated_template2 = translate_template(html_template2, lang_code)

    if 'lang_code' in session:
        lang_code = session['lang_code']
    else:
        lang_code = request.accept_languages.best_match(['en', 'fr', 'es', 'ta'])

    if a == 2:
        return render_template_string(translated_template2, lang_code=lang_code, default_value='')
    else:
        return render_template_string(translated_template1, lang_code=lang_code, default_value='')

@app.route('/app2')
def app2_index():
    # Route for the second page
    return render_template_string(html_template2, lang_code='en', default_value='')

@app.route('/app3')
def app3_index():
    # Route for the third page
    return render_template_string(html_template3, lang_code='en', default_value='')

if __name__ == '__main__':
    app.run(debug=True, port=5000)