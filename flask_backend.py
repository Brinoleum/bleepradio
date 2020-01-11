from src.process_lyrics import process_lyrics, output_processed
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
#http://127.0.0.1:5000/

@app.route('/')
def my_form():
    return render_template('text_box.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    # process_lyrics replaces swears with Simlish
    processed = process_lyrics(text)
    output_processed(processed)
    # so this should print the processed lyrics to the page
    # side effects: writes the text-to-speech binary mp3 to a file
    return processed

