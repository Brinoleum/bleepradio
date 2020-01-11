from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
#http://127.0.0.1:5000/

@app.route('/')
def my_form():
    return render_template('text_box.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper() #FIXME this will run the function that will modify the bleeps
    return processed_text