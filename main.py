from src.process_lyrics import NoCuss, random_bgm
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from google.cloud import storage
#import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'
bootstrap = Bootstrap(app)
#http://127.0.0.1:5000/

class LyricForm(FlaskForm):
    lyric = StringField('Search')

def hello():
    return "Hello"

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route('/', methods =['GET', 'POST'])
def my_form():
    form = LyricForm()
    if form.validate_on_submit():
        text = NoCuss(request.form['lyric'])
        processed = text.process_lyrics()
        name = text.song_name()
        text.output_processed(processed)
        return redirect(url_for('lyrics', lyric=processed, name=name))

    return render_template('text_box.html', form=form)

@app.route('/lyrics')
def lyrics():
    lyric = request.args.get('lyric', None)
    name = request.args.get('name', None)
    storage_client = storage.Client()
    bucket = storage_client.bucket("clean-264805.appspot.com")
    blob = bucket.blob("output.mp3")
    with open("/tmp/output.mp3", "wb+") as op:
        blob.download_to_file(op)
        template = render_template('Lyrics_page.html', lyric=lyric, name=name, bgm=random_bgm(), output = "/tmp/output.mp3")
    return template

if __name__ == '__main__':
    app.run(debug=True)
